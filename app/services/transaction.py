from datetime import datetime

import yfinance as yf

from app.models.asset import Asset
from app.repository.transaction import TransactionRepository
from app.schemas.asset import AssetResponse, AssetCreate
from app.schemas.transaction import TransactionResponse, TransactionBase, TransactionCreate
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

  async def create_transaction(self, portfolio_id: str, user_id: str, transaction: TransactionCreate) -> TransactionResponse:
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
    asset: Asset = await self.asset_service.get_asset_by_symbol(transaction.symbol, portfolio_id)
    if not asset:
      ticker = yf.Ticker(transaction.symbol)
      ticker_info = ticker.info

      add_new_asset = AssetCreate(
        symbol = ticker_info.get('symbol'),
        name = ticker_info.get('longName'),
        asset_type = ticker_info.get('quoteType'),
        sector = ticker_info.get('sector'),
        industry = ticker_info.get('industry'),
        currency = ticker_info.get('currency'),
        portfolio_id = portfolio_id,
      )
      asset: AssetResponse = await self.asset_service.create_asset(add_new_asset)

    #@TODO: IF the asset exists, update the asset with the new transaction data
    # Set dynamic values for the transaction and parse the date to a datetime object
    transaction.asset_id = asset.id
    transaction.portfolio_id = portfolio_id
    # transaction.created_at = datetime.strptime(str(transaction.created_at), '%Y-%m-%d %H:%M:%S%z')
    # transaction.created_at = transaction.created_at.strftime('%d-%m-%Y %H:%M:%S')
    # transaction.created_at = datetime.fromisoformat(transaction.created_at)
    transaction_data = Transaction(**transaction.model_dump(exclude={'symbol'}))

    result = await self.repository.add_transaction(transaction_data)
    transaction.id = str(result.inserted_id)
    return TransactionResponse(**transaction.model_dump())

  # async def create_transaction(self, transaction: TransactionBase) -> TransactionResponse:
  #   """
  #   Create a new transaction for an asset in the portfolio
  #   :param transaction: TransactionCreate
  #   :rtype: TransactionResponse
  #   """
  #   # Check if the portfolio exists
  #   portfolio = await self.portfolio_service.get_portfolio(transaction.portfolio_id, transaction.user_id)
  #   if not portfolio:
  #     raise ValueError('Portfolio not found...')
  #
  #   # Check if the asset exists in the portfolio by symbol
  #   try:
  #     asset: AssetResponse = await self.asset_service.get_asset_by_symbol(transaction.portfolio_id, transaction.symbol) # Need to have a get_asset_by_symbol method in the AssetService
  #   except ValueError as e:
  #     asset = None
  #
  #   if not asset:
  #     # Create a new asset if it doesn't exist
  #     add_new_asset = Asset(
  #       id=None,
  #       portfolio_id=transaction.portfolio_id,
  #       symbol=transaction.symbol,
  #       name=transaction.name,
  #       shares=transaction.shares,
  #       purchase_price=transaction.price,
  #       currency=transaction.currency,
  #       user_id=transaction.user_id
  #     )
  #     asset: AssetResponse = await self.asset_service.create_asset(add_new_asset)
  #   else:
  #     # Update the existing asset
  #     asset.shares += transaction.shares
  #     asset.purchase_price = transaction.price # For now we will just update the purchase price, but we should calculate the average price instead
  #     asset.currency = transaction.currency
  #     await self.asset_service.update_asset(asset)
  #
  #   transaction.asset_id = asset.id
  #
  #   transaction = Transaction(
  #     id=None,
  #     symbol=transaction.symbol,
  #     operation=transaction.operation,
  #     name=transaction.name,
  #     shares=transaction.shares,
  #     price=transaction.price,
  #     currency=transaction.currency,
  #     date=transaction.date,
  #     portfolio_id=transaction.portfolio_id,
  #     user_id=transaction.user_id,
  #     fee_tax=transaction.fee_tax,
  #     notes=transaction.notes
  #   )
  #
  #   await self.repository.add_transaction(transaction)
  #   return TransactionResponse(**transaction.model_dump())
  #
  # async def get_all_transactions(self, portfolio_id: str) -> list[TransactionResponse]:
  #   """
  #   Get all transactions for a portfolio
  #   :param portfolio_id: str
  #   :rtype: list[TransactionResponse]
  #   """
  #   transactions = await self.repository.get_transactions_by_portfolio(portfolio_id)
  #   return [TransactionResponse(**transaction.model_dump()) for transaction in transactions]
  #
  # async def update_transaction(self, transaction_id: str, transaction_data: TransactionBase) -> TransactionResponse:
  #   """
  #   Update a transaction
  #   :param transaction_data: TransactionBase
  #   :param transaction_id: str
  #   :rtype: TransactionResponse
  #   """
  #   transaction = await self.repository.get_transaction_by_id(transaction_id)
  #   if not transaction:
  #     raise ValueError('Transaction not found')
  #
  #   updated_transaction = transaction.copy(update=transaction_data.dict(exclude_unset=True))
  #   await self.repository.update_transaction(transaction_id, updated_transaction)
  #   return TransactionResponse(**updated_transaction.model_dump())
  #
  # async def delete_transaction(self, transaction_id: str) -> None:
  #   """
  #   Delete a transaction by its ID
  #   :param transaction_id: str
  #   :rtype: None
  #   """
  #   transaction = await self.repository.get_transaction_by_id(transaction_id)
  #   if not transaction:
  #     raise ValueError('Transaction not found')
  #   await self.repository.delete_transaction(transaction_id)
