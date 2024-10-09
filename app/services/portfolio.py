from typing import List, Dict, Any

import yfinance as yf

from app.models.asset import Asset
from app.models.portfolio import Portfolio
from app.repository.asset import AssetRepository
from app.repository.portfolio import PortfolioRepository
from app.schemas.asset import AssetResponse, PortfolioValueResponse
from app.schemas.portfolio import PortfolioResponse, PortfolioBase, PortfolioUpdate

class PortfolioService:
  """
  Portfolio service class to handle business logic for portfolios in the database
  """
  def __init__(self, portfolio_repository: PortfolioRepository, asset_repository: AssetRepository):
    self.repository = portfolio_repository
    self.asset_repository = asset_repository

  async def get_all_portfolio(self, current_user_id: str) -> list[PortfolioResponse]:
    """
    Get all portfolios from the database
    # :param current_user_id: str
    :return: list[PortfolioResponse]
    """
    portfolios = await self.repository.get_all_portfolios(current_user_id)
    if portfolios:
      return [PortfolioResponse(**portfolio.model_dump()) for portfolio in portfolios]
    raise ValueError('No portfolios found...')

  async def create_portfolio(self, portfolio: PortfolioBase, current_user_id: str) -> PortfolioResponse:
    """
    Create a new portfolio in the database
    :param portfolio: PortfolioCreate
    :param current_user_id: str
    :return: PortfolioResponse
    """

    # Validate the portfolio data
    portfolio = Portfolio(
      name = portfolio.name,
      description = portfolio.description,
      sets=[Asset(**asset.model_dump()) for asset in portfolio.assets] if portfolio.assets else [],
      user_id = current_user_id,
      strategy = portfolio.strategy
    )

    await self.repository.add_portfolio(portfolio)

    return PortfolioResponse(**portfolio.model_dump())

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
    portfolio = await self.repository.get_portfolio_by_id(portfolio_id)
    if not portfolio:
      raise ValueError('Portfolio not found...')

    if portfolio.user_id != user_id:
      raise ValueError('You do not have permission to update this portfolio...')

    updated_portfolio = await self.repository.update_portfolio(portfolio_id, portfolio_data.model_dump(exclude_unset=True))
    return PortfolioResponse(**updated_portfolio.model_dump())

  async def delete_portfolio(self, portfolio_id: str, user_id: str):
    """
    Delete a portfolio from the database
    :param portfolio_id: str
    :param user_id: str
    :return: None
    """
    portfolio = await self.repository.get_portfolio_by_id(portfolio_id)
    if not portfolio:
      raise ValueError('Portfolio not found...')

    if portfolio.user_id != user_id:
      raise ValueError('You do not have permission to delete this portfolio...')

    await self.repository.delete_portfolio(portfolio_id)

  async def get_portfolio(self, portfolio_id: str, user_id: str) -> PortfolioResponse:
    """
    Get a portfolio by id
    :param portfolio_id: str
    :param user_id: str
    :return: PortfolioResponse
    """
    portfolio = await self.repository.get_portfolio_by_id(portfolio_id)
    if not portfolio:
      raise ValueError('Portfolio not found...')

    if portfolio.user_id != user_id:
      raise ValueError('You do not have permission to view this portfolio...')

    # Fetch the assets linked to the portfolio
    assets = await self.asset_repository.get_all_assets(portfolio_id, user_id)
    asset_responses = [AssetResponse(**asset.model_dump()) for asset in assets]

    # Include assets in the PortfolioResponse
    return PortfolioResponse(**portfolio.model_dump(exclude={"assets"}), assets=asset_responses)

  async def calculate_portfolio_value(self, portfolio_id: str, user_id: str) -> PortfolioValueResponse:
    """
    Calculate the value of a portfolio
    :param portfolio_id:
    :param user_id:
    :return:
    """
    portfolio = await self.get_portfolio(portfolio_id, user_id)

    total_investment = 0
    total_value = 0

    for asset in portfolio.assets:
      total_investment += asset.purchase_price * asset.shares
      stock = yf.Ticker(asset.symbol)
      stock_price = stock.history(period='1d')['Close'].values[0]
      total_value += stock_price * asset.shares

    return_percentage = ((total_value - total_investment) / total_investment) * 100 if total_investment > 0 else 0

    return PortfolioValueResponse(
      total_investment=total_investment,
      total_value=float(total_value),
      return_percentage=float(return_percentage)
    )

  async def get_portfolio_by_id(self, portfolio_id: str) -> Portfolio:
    """
    Get a portfolio by id
    :param portfolio_id: str
    :return: Portfolio
    """
    portfolio = await self.repository.get_portfolio_by_id(portfolio_id)
    if not portfolio:
      raise ValueError('Portfolio not found...')

    return portfolio
