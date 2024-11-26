from bson import ObjectId

from app.core.database import db
from app.models.portfolio import Portfolio

class PortfolioRepository:
  """
    A class to represent a portfolio repository, and contains
    methods to interact with the database.
  """
  def __init__(self) -> None:
    self.collection = db.get_collection('portfolios')

  async def fetch_all_portfolios(self, user_id: str) -> list[Portfolio]:
    """
    Fetch all portfolios in the database from the current user
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
      return await self.collection.insert_one(portfolio.model_dump())
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
      updated_portfolio['id'] = str(updated_portfolio['_id'])
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
