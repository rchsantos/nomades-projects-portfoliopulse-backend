# Import necessary libraries
import logging
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import yfinance as yf
from pymongo.results import InsertOneResult

# Import necessary modules App
from app.models.portfolio import Portfolio
from app.repository.portfolio import PortfolioRepository
from app.schemas.asset import AssetUpdate, AssetResponse
from app.schemas.portfolio import PortfolioResponse, PortfolioUpdate, PortfolioCreate, PortfolioAnalysisResponse, \
    WeightDetail
from app.schemas.transaction import TransactionResponse
from app.services.asset import AssetService

# Import necessary modules machine learning
from app.machine_learning.data_processing import prepare_lstm_data
from app.machine_learning.lstm import build_lstm_model, predict_future_prices


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

    async def get_lstm_predictions_for_holdings(self, portfolio_id: str, user_id: str, days: int) -> dict :
        """
        Predict future prices for all holdings in a portfolio using LSTM.
        :param portfolio_id: Portfolio ID
        :param user_id: The current authenticated user ID
        :param days: Number of days to predict for each holding.
        :return: Dictionary with predictions for each holding in the portfolio
        """
        predictions = {}

        # Check if the portfolio exists
        portfolio = await self.get_portfolio(portfolio_id, user_id)
        if not portfolio:
            raise ValueError('Portfolio not found...')

        holdings = await self.fetch_portfolio_holdings(portfolio_id, user_id)
        if not holdings:
            raise ValueError('No holdings found for the portfolio...')

        for holding in holdings:
            try:
                # Fetch historical prices for the asset
                df: pd.DataFrame = await self.fetch_historical_data(holding.symbol)
                if df.empty:
                    raise ValueError(f'No historical data found for {holding.symbol}...')

                # Extract the closing prices
                close_prices = df['Close'].values

                # Prepare the data for LSTM
                X, _, scaler = prepare_lstm_data(close_prices)

                # Build and train the LSTM model
                model = build_lstm_model((X.shape[1], 1))
                model.fit(X, X, epochs=80, batch_size=8, verbose=1)

                model.summary()

                # Predict future prices
                last_sequence = X[-1] # Last sequence in the dataset
                holding_predictions = predict_future_prices(model, last_sequence, scaler, days)

                # Convert predictions to native Python types (e.g., float)
                holding_predictions = [float(pred) for pred in holding_predictions]

                # Store the predictions for the holding
                predictions[holding.symbol] = holding_predictions

            except Exception as e:
                logging.error(f'Error predicting prices for {holding.symbol}: {str(e)}')
                predictions[holding.symbol] = {f"error": str(e)}

        return predictions

    async def get_lstm_predictions_for_asset(self, portfolio_id: str, symbol: str, user_id: str,  days: int) -> dict:
        """
        Predict future prices for a specific asset in a portfolio using LSTM.
        :param symbol: Asset symbol (e.g., "AAPL" for Apple).
        :param user_id: The current authenticated user ID
        :param portfolio_id: Portfolio ID
        :param days: Number of days to predict for the asset.
        :return: List of predicted prices for the asset
        """
        try:
            # Check if the portfolio exists
            portfolio = await self.get_portfolio(portfolio_id, user_id)
            if not portfolio:
                raise ValueError('Portfolio not found...')

            # Fetch holdings for the portfolio
            holdings = await self.fetch_portfolio_holdings(portfolio_id, user_id)
            if not holdings:
                raise ValueError('No holdings found for the portfolio...')

            # Find the holding with the specified asset ID
            holding = next((h for h in holdings if h.symbol == symbol), None)
            if not holding:
                raise ValueError(f'Asset {symbol} not found in the portfolio...')

            # Fetch historical prices for the asset
            df: pd.DataFrame = await self.fetch_historical_data(symbol) # @TODO: Implement the choice of the date range
            if df.empty:
                raise ValueError(f'No historical data found for {symbol}...')

            # Extract the closing prices
            close_prices = df['Close'].values

            # Prepare the data for LSTM
            X, _, scaler = prepare_lstm_data(close_prices)

            # Build and train the LSTM model
            model = build_lstm_model((X.shape[1], 1))
            model.fit(X, X, epochs=80, batch_size=8, verbose=1)

            model.summary()

            # Predict future prices
            last_sequence = X[-1]  # Last sequence in the dataset
            predictions = predict_future_prices(model, last_sequence, scaler, days)

            # Convert predictions to native Python types (e.g., float)
            predictions = [float(pred) for pred in predictions]

            today = datetime.now()
            predictions_dates = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days)]

            return {
                'symbol': symbol,
                'dates': predictions_dates,
                'predictions': predictions
            }

        except Exception as e:
            logging.error(f'Error predicting prices for {symbol}: {str(e)}')
            return {f"error": str(e)}

    async def fetch_historical_data(self, ticker: str, start_date: str = '2018-01-01', end_date: str = '2024-12-12') -> pd.DataFrame:
        """
        Fetch and clean historical data for a given asset (ticker) using yfinance.
        :param ticker: Asset symbol (e.g., "AAPL" for Apple).
        :param start_date: Start date for the historical data (format: YYYY-MM-DD).
        :param end_date: End date for the historical data (format: YYYY-MM-DD).
        :return: Pandas DataFrame containing cleaned historical data.
        """
        try:
            # fetch raw data from Yahoo Finance
            data = yf.download(ticker, start=start_date, end=end_date)

            # If no data is returned, raise an exception
            if data.empty:
                raise ValueError(f'No historical data found for {ticker}...')

            # Convert Dataframe and clean data
            df = data[['Open', 'High', 'Low', 'Close', 'Volume']].reset_index()
            df['Close'] = df['Close'].ffill() # Fill missing values with the previous day's close price
            df = df[df['Close'] > 0] # Remove rows with zero or negative close prices


            return df
        except Exception as e:
            logging.error(f'Error fetching historical data for {ticker}: {str(e)}')
            return pd.DataFrame()
