from bson import ObjectId
from sqlalchemy.testing.plugin.plugin_base import logging

from app.core.database import db

from app.models.transaction import Transaction

class TransactionRepository:
    """
    TransactionRepository class is responsible for handling all the database operations related to transaction
    """
    def __init__(self):
        self.collection = db.get_collection('transactions')

    async def add_transaction(self, transaction: Transaction) -> Transaction:
        """
        Add a new transaction to the database
        :param transaction: Transaction
        :rtype: Transaction
        """
        try:
            return await self.collection.insert_one(transaction.model_dump())
        except Exception as e:
          logging.error(f'Error adding transaction: {e}')
          raise ValueError(str(e))

    async def fetch_transactions_from_portfolio(self, portfolio_id: str):
        """
        Fetch all transactions for a portfolio
        :param portfolio_id: str
        :rtype: list[Transaction]
        """
        try:
            cursor = self.collection.find({'portfolio_id': portfolio_id})
            transactions = []
            async for transaction in cursor:
                transaction['id'] = str(transaction['_id'])
                transactions.append(Transaction(**transaction))
            return transactions
        except Exception as e:
            logging.error(f'Error fetching transactions: {e}')
            raise ValueError(str(e))

    async def update_transaction(self, transaction_id: str, updated_transaction: dict) -> None:
        """
        Update an existing transaction in the database
        :param transaction_id: str
        :param updated_transaction: Transaction
        :rtype: None
        """
        try:
            await self.collection.update_one(
                {'_id': ObjectId(transaction_id)},
                {
                    '$set': updated_transaction,
                    '$currentDate': {'lastUpdated': True}
                }
            )

            updated_transaction = await self.collection.find_one({'_id': ObjectId(transaction_id)})
            updated_transaction['id'] = str(updated_transaction['_id'])
            return updated_transaction
        except Exception as e:
            logging.error(f'Error updating transaction: {e}')
            raise ValueError(str(e))

    async def find_transaction_by_id(self, transaction_id: str) -> Transaction:
        """
        Find a transaction by its ID
        :param transaction_id: str
        :rtype: Transaction
        """
        try:
            transaction = await self.collection.find_one({'_id': ObjectId(transaction_id)})
            return Transaction(**transaction)
        except Exception as e:
            logging.error(f'Error finding transaction: {e}')
            raise ValueError(str(e))

    async def delete_transaction(self, transaction_id: str) -> None:
        """
        Delete a transaction from the database
        :param transaction_id: str
        :rtype: None
        """
        try:
            await self.collection.delete_one({'_id': ObjectId(transaction_id)})
        except Exception as e:
            logging.error(f'Error deleting transaction: {e}')
            raise ValueError(str(e))
