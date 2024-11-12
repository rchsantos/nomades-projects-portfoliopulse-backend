from bson import ObjectId

from app.core.database import db
import app.schemas.portfolio as portfolio_schema
from app.models.portfolio import Portfolio

class PortfolioRepository:
  """
    A class to represent a portfolio repository, and contains
    methods to interact with the database.
  """
  def __init__(self) -> None:
    self.collection = db.get_collection('portfolios')
    self.portfolio_schema = portfolio_schema

  async def fetch_all_portfolios(self, user_id: str) -> list[Portfolio]:
    """
    Get all portfolios in the database from the current user
    """
    portfolio_cursor = self.collection.find({'user_id': user_id})
    portfolios = []
    async for portfolio in portfolio_cursor:
      portfolio['id'] = str(portfolio['_id'])
      portfolios.append(Portfolio(**portfolio))
    return portfolios

  async def add_portfolio(self, portfolio: Portfolio) -> Portfolio:
    """
    Add a new portfolio to the database
    """
    try:
      portfolio_dict = portfolio.model_dump()
      # result =
      # portfolio.id = str(result.inserted_id)
      return await self.collection.insert_one(portfolio_dict)
    except Exception as e:
      raise ValueError(str(e))

  async def update_portfolio(self, portfolio_id: str, portfolio: dict) -> Portfolio:
    """
    Update a portfolio in the database
    :param portfolio_id: str
    :param portfolio: PortfolioUpdate
    :return: Portfolio
    """
    try:
      await self.collection.update_one(
        {'_id': ObjectId(portfolio_id)},
        {
          '$set': portfolio,
          '$currentDate': {'lastUpdated': True}
        }
      )
      updated_portfolio = await self.collection.find_one({'_id': ObjectId(portfolio_id)})
      return updated_portfolio
    except Exception as e:
      raise ValueError(str(e))

  async def delete_portfolio(self, portfolio_id: str) -> None:
    """
    Delete a portfolio from the database
    :param portfolio_id: str
    :return: None
    """
    try:
      await self.collection.delete_one({'_id': ObjectId(portfolio_id)})
    except Exception as e:
      raise ValueError(str(e))


  async def find_portfolio_by_id(self, portfolio_id: str) -> Portfolio:
    """
    Find a portfolio by id
    :param portfolio_id: str
    :return: dict
    """
    portfolio = await self.collection.find_one({'_id': ObjectId(portfolio_id)})
    return portfolio

  #
  # def get_portfolio_by_user(self, user_id: str) -> list[dict]:
  #   """
  #   Get all portfolios by user
  #   """
  #   return [portfolio.to_dict() for portfolio in self.collection.where(
  #     filter = FieldFilter(
  #       u'user_id',
  #       u'==',
  #       user_id
  #     )
  #   ).get()]
  #
  # @staticmethod
  # def portfolio_to_firestore(portfolio: Portfolio) -> dict:
  #   return {
  #     u'id': portfolio.id,
  #     u'name': portfolio.name,
  #     u'description': portfolio.description,
  #     u'assets': portfolio.assets,
  #     u'user_id': portfolio.user_id,
  #     u'strategy': portfolio.strategy,
  #     u'currency': portfolio.currency
  #   }
  #
  # @staticmethod
  # def firestore_to_portfolio(portfolio_document: DocumentSnapshot) -> Portfolio:
  #   portfolio_data = portfolio_document.to_dict()
  #   return Portfolio(
  #     id = portfolio_document.id,
  #     name = portfolio_data['name'],
  #     description = portfolio_data['description'],
  #     assets = portfolio_data['assets'] if 'assets' in portfolio_data else [],
  #     user_id = portfolio_data['user_id'],
  #     strategy = portfolio_data['strategy'],
  #     currency = portfolio_data['currency'] if 'currency' in portfolio_data else None
  #   )
