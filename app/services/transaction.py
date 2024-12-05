from datetime import datetime

import yfinance as yf

from app.models.asset import Asset
from app.repository.transaction import TransactionRepository
from app.schemas.asset import AssetResponse, AssetCreate
from app.schemas.transaction import TransactionResponse, TransactionBase, TransactionCreate, TransactionUpdate
from app.services.asset import AssetService
from app.services.portfolio import PortfolioService
from app.models.transaction import Transaction


class TransactionService:
    """
    This class will contain all the business logic for the transaction
    """
    def __init__(
        self,
        repository: TransactionRepository,
        portfolio_service: PortfolioService,
        asset_service: AssetService):
        self.repository = repository
        self.portfolio_service = portfolio_service
        self.asset_service = asset_service

    async def create_transaction(self,
                                 portfolio_id: str,
                                 user_id: str,
                                 transaction: TransactionCreate) -> TransactionResponse:
        """
        Create a new transaction for an asset in the portfolio
        :param user_id:
        :param portfolio_id: str
        :param transaction: TransactionBase
        :return: TransactionResponse
        """
        # Check if the portfolio exists
        portfolio = await self.portfolio_service.get_portfolio(portfolio_id, user_id)
        if not portfolio:
            raise ValueError('Portfolio not found...')

        # Check if the asset exists in the portfolio by symbol, if not create a new asset
        asset: Asset = await self.asset_service.get_asset_by_symbol(transaction.symbol)
        asset_id = None
        if not asset:
            ticker = yf.Ticker(transaction.symbol)
            ticker_info = ticker.info

            add_new_asset = AssetCreate(
                symbol=ticker_info.get('symbol'),
                name=ticker_info.get('longName'),
                asset_type=ticker_info.get('quoteType'),
                sector=ticker_info.get('sector'),
                industry=ticker_info.get('industry'),
                currency=ticker_info.get('currency'),
                portfolio_id=portfolio_id,
            )
            asset: AssetResponse = await self.asset_service.create_asset(add_new_asset)
            asset_id = asset.id
        else:
            asset_id = str(asset['_id'])

        # Set dynamic values for the transaction and parse the date to a datetime object
        transaction.asset_id = asset_id
        transaction.portfolio_id = portfolio_id
        transaction_data = Transaction(**transaction.model_dump(exclude={'symbol'}))

        result = await self.repository.add_transaction(transaction_data)
        transaction.id = str(result.inserted_id)
        return TransactionResponse(**transaction.model_dump())

    async def fetch_all_transactions(self, portfolio_id: str, user_id: str) -> list[TransactionResponse]:
        """
        @TODO: Check if this method is necessary, since we have a recollection method to retrieve all transactions of a portfolio in the portfolio service
        Get all transactions for a portfolio
        :param user_id: str
        :param portfolio_id: str
        :rtype: list[TransactionResponse]
        """
        portfolio = await self.portfolio_service.get_portfolio(portfolio_id, user_id)
        if not portfolio:
            raise ValueError('Portfolio not found...')

        transactions = await self.repository.fetch_transactions_from_portfolio(portfolio_id)
        return [TransactionResponse(**transaction.model_dump()) for transaction in transactions]

    async def update_transaction(
        self,
        portfolio_id: str,
        user_id: str,
        transaction_id: str,
        transaction_data: TransactionUpdate) -> TransactionResponse:
        """
        Update a transaction
        :param user_id:
        :param portfolio_id:
        :param transaction_data: TransactionBase
        :param transaction_id: str
        :rtype: TransactionResponse
        """
        portfolio = await self.portfolio_service.get_portfolio(portfolio_id, user_id)
        if not portfolio:
            raise ValueError('Portfolio not found...')

        transaction = await self.repository.find_transaction_by_id(transaction_id)
        if not transaction:
            raise ValueError('Transaction not found')

        updated_transaction = await self.repository.update_transaction(transaction_id, transaction_data.model_dump(exclude_unset=True))
        return TransactionResponse(**updated_transaction)

    async def delete_transaction(
        self,
        portfolio_id: str,
        user_id: str,
        transaction_id: str) -> None:
        """
        Delete a transaction by its ID
        :param user_id:
        :param portfolio_id:
        :param transaction_id: str
        :rtype: None
        """
        portfolio = await self.portfolio_service.get_portfolio(portfolio_id, user_id)
        if not portfolio:
            raise ValueError('Portfolio not found...')

        transaction = await self.repository.find_transaction_by_id(transaction_id)
        if not transaction:
            raise ValueError('Transaction not found')

        await self.repository.delete_transaction(transaction_id)
