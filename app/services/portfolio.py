import yfinance as yf

from app.models.asset import Asset
from app.models.portfolio import Portfolio
from app.repository.portfolio import PortfolioRepository
from app.schemas.portfolio import PortfolioResponse, PortfolioUpdate, PortfolioCreate
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
        result = await self.repository.add_portfolio(portfolio)
        portfolio.id = str(result.inserted_id)
        portfolio_assets_ids = []

        # Second, create the assets linked to the portfolio
        if portfolio.assets:
            for asset in portfolio.assets:
                # Check if the asset exists in the database
                existing_asset = await self.asset_service.get_asset_by_symbol(asset['symbol'])
                if existing_asset:
                    existing_asset['portfolio_ids'].append(portfolio.id)
                    await self.asset_service.update_asset(existing_asset['_id'], existing_asset)
                    portfolio_assets_ids.append(existing_asset['id'])
                else:
                    asset['portfolio_ids'] = []
                    asset['portfolio_ids'].append(portfolio.id)
                    asset_result = await self.asset_service.create_asset(asset)
                    portfolio_assets_ids.append(str(asset_result.id))

        # Update the portfolio with the asset ids
        portfolio = await self.repository.update_portfolio(portfolio.id, {"assets": portfolio_assets_ids})

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
        return PortfolioResponse(**updated_portfolio.model_dump())

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

        # Fetch the assets linked to the portfolio
        # assets = await self.asset_repository.get_all_assets(portfolio_id, user_id)
        # asset_responses = [AssetResponse(**asset.model_dump()) for asset in assets]

        # Include assets in the PortfolioResponse
        return PortfolioResponse(**portfolio)
        # return PortfolioResponse(**portfolio.model_dump(exclude={"assets"}), assets=asset_responses)

    # async def calculate_portfolio_value(self, portfolio_id: str, user_id: str) -> PortfolioValueResponse:
    #   """
    #   Calculate the value of a portfolio
    #   :param portfolio_id:
    #   :param user_id:
    #   :return:
    #   """
    #   portfolio = await self.get_portfolio(portfolio_id, user_id)
    #
    #   total_investment = 0
    #   total_value = 0
    #
    #   for asset in portfolio.assets:
    #     total_investment += asset.purchase_price * asset.shares
    #     stock = yf.Ticker(asset.symbol)
    #     stock_price = stock.history(period='1d')['Close'].values[0]
    #     total_value += stock_price * asset.shares
    #
    #   return_percentage = ((total_value - total_investment) / total_investment) * 100 if total_investment > 0 else 0
    #
    #   return PortfolioValueResponse(
    #     total_investment=total_investment,
    #     total_value=float(total_value),
    #     return_percentage=float(return_percentage)
    #   )
