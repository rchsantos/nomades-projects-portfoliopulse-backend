from app.models.portfolio import Portfolio
from app.repository.portfolio import PortfolioRepository
from app.schemas.portfolio import PortfolioResponse, PortfolioBase, PortfolioUpdate

class PortfolioService:
  """
  Portfolio service class to handle business logic for portfolios in the database
  """

  def __init__(self, repository: PortfolioRepository):
    self.repository = repository

  async def get_all_portfolio(self, current_user_id: str) -> list[PortfolioResponse]:
    """
    Get all portfolios from the database
    :param current_user_id: str
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
      tickers = portfolio.tickers,
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
    portfolio = self.repository.get_portfolio_by_id(portfolio_id)
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
    portfolio = self.repository.get_portfolio_by_id(portfolio_id)
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

    return PortfolioResponse(**portfolio.model_dump())
