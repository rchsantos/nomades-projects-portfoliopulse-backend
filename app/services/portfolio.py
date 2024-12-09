import logging
import pandas as pd
import yfinance as yf
from pymongo.results import InsertOneResult

from app.models.portfolio import Portfolio
from app.repository.portfolio import PortfolioRepository
from app.schemas.asset import AssetUpdate, AssetResponse
from app.schemas.portfolio import PortfolioResponse, PortfolioUpdate, PortfolioCreate, PortfolioAnalysisResponse, \
    WeightDetail
from app.schemas.transaction import TransactionResponse
from app.services.asset import AssetService

class PortfolioService:
    """
    Portfolio service class to handle business logic for portfolios in the database
    """
    def __init__(self, portfolio_repository: PortfolioRepository, asset_service: AssetService):
        self.repository = portfolio_repository
        self.asset_service = asset_service

    async def get_all_portfolio(self, current_user_id: str) -> list[PortfolioResponse]:
        """
        Get all portfolios from the database
        # :param current_user_id: str
        :return: list[PortfolioResponse]
        """
        portfolios: list[Portfolio] = await self.repository.fetch_all_portfolios(current_user_id)
        if portfolios:
            return [PortfolioResponse(**portfolio.model_dump()) for portfolio in portfolios]
        raise ValueError('No portfolios found...')

    async def create_portfolio(self, portfolio: PortfolioCreate, user_id: str) -> PortfolioResponse:
        """
        Create a new portfolio in the database
        :param portfolio: PortfolioCreate
        :param user_id: str
        :return: PortfolioResponse
        """
        # First, create the portfolio
        portfolio.user_id = user_id
        portfolio = Portfolio(**portfolio.model_dump())
        result: InsertOneResult = await self.repository.add_portfolio(portfolio)
        portfolio.id = str(result.inserted_id)
        portfolio_assets_ids = []

        # Second, create the assets linked to the portfolio
        if portfolio.assets:
            for asset in portfolio.assets:
                # Check if the asset exists in the database
                existing_asset = await self.asset_service.get_asset_by_symbol(asset['symbol'])
                if existing_asset:
                    existing_asset['portfolio_ids'].append(portfolio.id)
                    existing_asset_to_update = AssetUpdate(**existing_asset)
                    await self.asset_service.update_asset(str(existing_asset['_id']), existing_asset_to_update)
                    portfolio_assets_ids.append(str(existing_asset['_id']))
                else:
                    asset['portfolio_ids'] = []
                    asset['portfolio_ids'].append(portfolio.id)
                    asset_result = await self.asset_service.create_asset(asset)
                    portfolio_assets_ids.append(str(asset_result.id))

        # Update the portfolio with the asset ids
        portfolio: Portfolio = await self.repository.update_portfolio(portfolio.id, {"assets": portfolio_assets_ids})

        return PortfolioResponse(**portfolio)

    async def update_portfolio(
        self,
        portfolio_id: str,
        portfolio_data: PortfolioUpdate,
        user_id: str
    ) -> PortfolioResponse:
        """
        Update a portfolio in the database
        :param portfolio_data: PortfolioUpdate
        :param portfolio_id: str
        :param user_id: str
        :return: PortfolioResponse
        """
        portfolio = await self.repository.find_portfolio_by_id(portfolio_id)
        if not portfolio:
            raise ValueError('Portfolio not found...')

        if portfolio['user_id'] != user_id:
            raise ValueError('You do not have permission to update this portfolio...')

        updated_portfolio = await self.repository.update_portfolio(portfolio_id,
                                                                   portfolio_data.model_dump(exclude_unset=True))
        return PortfolioResponse(**updated_portfolio)

    async def delete_portfolio(self, portfolio_id: str, user_id: str):
        """
        Delete a portfolio from the database
        :param portfolio_id: str
        :param user_id: str
        :return: None
        """
        portfolio = await self.repository.find_portfolio_by_id(portfolio_id)
        if not portfolio:
            raise ValueError('Portfolio not found...')

        if portfolio['user_id'] != user_id:
            raise ValueError('You do not have permission to delete this portfolio...')

        await self.repository.delete_portfolio(portfolio_id)

    async def get_portfolio(self, portfolio_id: str, user_id: str) -> PortfolioResponse:
        """
        Get a portfolio by id
        :param portfolio_id: str
        :param user_id: str
        :return: PortfolioResponse
        """
        portfolio = await self.repository.find_portfolio_by_id(portfolio_id)
        if not portfolio:
            raise ValueError('Portfolio not found...')

        # Check if the user has permission to view the portfolio
        if portfolio['user_id'] != user_id:
            raise ValueError('You do not have permission to view this portfolio...')

        portfolio['id'] = str(portfolio['_id'])

        # Include assets in the PortfolioResponse
        return PortfolioResponse(**portfolio)
        # return PortfolioResponse(**portfolio.model_dump(exclude={"assets"}), assets=asset_responses)

    async def fetch_portfolio_holdings(self, portfolio_id: str, user_id: str) -> list[AssetResponse]:
        """
        @TODO: Verify if this method is still needed
        Fetch all holdings from the database for the given portfolio ID.
        :param user_id: str
        :param portfolio_id: str
        :return: list[AssetResponse]
        """
        # Check if the portfolio exists
        portfolio: Portfolio = await self.repository.find_portfolio_by_id(portfolio_id)
        if not portfolio:
            raise ValueError('Portfolio not found...')

        # Check if the user has permission to view the portfolio
        if portfolio['user_id'] != user_id:
            raise ValueError('You do not have permission to view this portfolio...')

        # Get all assets linked to the portfolio
        holdings = []
        if portfolio['assets']:
            for asset_id in portfolio['assets']:
                asset = await self.asset_service.get_asset_by_id(asset_id)
                holdings.append(asset)

        if not holdings:
            raise ValueError('No holdings found for the portfolio...')

        # Return object with the holdings and the portfolio
        return [AssetResponse(**asset.model_dump()) for asset in holdings]

    async def get_asset_current_price(self, symbol: str) -> float:
        """
        Fetch the current price of an asset using yfinance.
        :param symbol: str
        :return: float
        """
        try:
            ticker = yf.Ticker(symbol)
            return ticker.history(period='1d')['Close'].iloc[-1]
        except Exception as e:
            logging.error(f'Error fetching asset price: {e}')
            return 0.0

    async def calculate_portfolio_analysis(self, portfolio_id: str, user_id: str):
        """
        Perform financial analysis on the portfolio's holdings.
        Calculate total value and asset weights.
        :param portfolio_id: str
        :param user_id: str
        :return:
        """
        # Fetch all assets linked to the portfolio
        assets = await self.fetch_portfolio_holdings(portfolio_id, user_id)
        if not assets:
            raise ValueError('No assets found for the portfolio...')

        # Fetch all transactions linked to the portfolio
        transactions = await self.fetch_all_transactions(portfolio_id, user_id)
        if not transactions:
            raise ValueError('No transactions found for the portfolio...')

        # Group transactions by asset
        transactions_by_asset = {}
        for transaction in transactions:
            if transaction.asset_id not in transactions_by_asset:
                transactions_by_asset[transaction.asset_id] = []
            transactions_by_asset[transaction.asset_id].append(transaction)

        # Create a list of holdings with the assets and their transactions for DataFrame conversion
        holdings = []
        for asset in assets:
            asset_transactions = transactions_by_asset.get(asset.id, [])
            # Calculate total shares and weighted average price for the asset
            total_shares = sum(tx.shares for tx in asset_transactions)
            total_cost = sum(tx.shares * tx.price_per_share for tx in asset_transactions)
            average_price = total_cost / total_shares if total_shares else 0

            # Fetch current price using yfinance
            current_price = await self.get_asset_current_price(asset.symbol)

            # Calculate total value and weight for the asset
            current_value = total_shares * current_price

            # Append the holding information to the list
            holdings.append({
                'asset': asset,
                'quantity': total_shares,
                'current_value': current_value,
                'current_price': current_price
            })

        # Convert holdings to a DataFrame
        df = pd.DataFrame(holdings)

        # Check if current_value is present to proceed with analysis
        if 'current_value' not in df.columns or df['current_value'].sum() == 0:
            raise ValueError('Unable to calculate portfolio analysis: no valid current values available.')

        # Perform financial analysis
        df['weight'] = df['current_value'] / df['current_value'].sum()

        # Prepare the analysis result
        weights = [
            WeightDetail(asset=row['asset'], quantity=row['quantity'],current_value=row['current_value'], weight=row['weight'])
            for _, row in df.iterrows()
        ]
        total_value = df['current_value'].sum()

        return PortfolioAnalysisResponse(total_value=total_value, weights=weights)


    async def fetch_all_transactions(self, portfolio_id: str, user_id: str):
        """
        Fetch all transactions for a portfolio
        :param user_id: str
        :param portfolio_id: str
        :return: list[TransactionResponse]
        """
        # Check if the portfolio exists
        portfolio = await self.get_portfolio(portfolio_id, user_id)
        if not portfolio:
            raise ValueError('Portfolio not found...')

        transactions = await self.repository.fetch_all_transactions(portfolio_id)
        return [TransactionResponse(**transaction.model_dump()) for transaction in transactions]

