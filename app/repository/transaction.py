from google.cloud.firestore_v1 import DocumentSnapshot, FieldFilter

from app.core.firestore_db import db

from app.models.transaction import Transaction

class TransactionRepository:
    """
    TransactionRepository class is responsible for handling all the database operations related to transaction
    """
    def __init__(self):
        self.collection = db.collection('transactions')

    async def add_transaction(self, transaction: Transaction) -> Transaction:
        """
        Add a new transaction to the database
        :param transaction: Transaction
        :rtype: Transaction
        """
        try:
          _, transaction_ref = self.collection.add(self.transaction_to_firestore(transaction))
          transaction.id = transaction_ref.id
          return transaction
        except Exception as e:
          raise ValueError(str(e))

    async def get_transactions_by_portfolio(self, portfolio_id: str) -> list[Transaction]:
      """
      Get all transactions for a portfolio
      :param portfolio_id: str
      :rtype: list[Transaction]
      """
      try:
        transactions = self.collection.where(
          filter = FieldFilter(
            'portfolio_id',
            '==',
            portfolio_id
          )
        ).get()
        return [self.firestore_to_transaction(transaction) for transaction in transactions]
      except Exception as e:
        raise ValueError(str(e))

    @staticmethod
    def transaction_to_firestore(transaction: Transaction) -> dict:
        """
        Convert a transaction object to a dictionary
        :param transaction: Transaction
        :rtype: dict
        """
        return {
          u'id': transaction.id,
          u'portfolio_id': transaction.portfolio_id,
          u'asset_id': transaction.asset_id,
          u'symbol': transaction.symbol,
          u'operation': transaction.operation,
          u'shares': transaction.shares,
          u'price': transaction.price,
          u'currency': transaction.currency,
          u'date': transaction.date,
          u'fee_tax': transaction.fee_tax,
          u'notes': transaction.notes
        }

    @staticmethod
    def firestore_to_transaction(transaction_document: DocumentSnapshot) -> Transaction:
      transaction_data = transaction_document.to_dict()
      return Transaction(
        id=transaction_document.id,
        portfolio_id=transaction_data['portfolio_id'],
        symbol=transaction_data['symbol'],
        operation=transaction_data['operation'],
        shares=transaction_data['shares'],
        price=transaction_data['price'],
        currency=transaction_data['currency'],
        date=transaction_data['date'],
        asset_id=transaction_data['asset_id'],
        fee_tax=transaction_data['fee_tax'],
        notes=transaction_data['notes']
      )
