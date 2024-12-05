import logging
from fastapi import (
  APIRouter,
  HTTPException,
  Depends
)

# from app.schemas.asset import PortfolioValueResponse
from app.schemas.portfolio import PortfolioResponse, PortfolioBase, PortfolioUpdate, PortfolioCreate, \
    PortfolioHoldingsResponse, PortfolioAnalysisResponse
from app.schemas.user import UserResponse
from app.services.portfolio import PortfolioService
from app.dependencies import get_portfolio_service, get_current_user

router = APIRouter(
  prefix='/portfolio',
  tags=['portfolio']
)
#
@router.get(
  '/',
  response_model=list[PortfolioResponse],
  status_code=200,
  description='Get all portfolios of the current user from the database',
  response_description='Portfolios retrieved successfully'
)
async def get_all_portfolio(
  portfolio_service: PortfolioService = Depends(get_portfolio_service),
  current_user: UserResponse = Depends(get_current_user),
):
  user = await current_user
  try:
    return await portfolio_service.get_all_portfolio(user.id)
  except ValueError as e:
    logging.error(f"Error getting all portfolios: {e}")
    raise HTTPException(status_code=404, detail=str(e))

@router.post(
  '/',
  response_model=PortfolioResponse,
  status_code=201,
  description='Create a new portfolio of the current user in the database',
  response_description='Portfolio created successfully'
)
async def create_portfolio(
  portfolio: PortfolioCreate,
  portfolio_service: PortfolioService = Depends(get_portfolio_service),
  current_user: UserResponse = Depends(get_current_user),
):
  try:
    user = await current_user
    return await portfolio_service.create_portfolio(portfolio, user.id)
  except ValueError as e:
    logging.error(f'Error creating portfolio: {e}')
    raise HTTPException(status_code=400, detail=str(e))

@router.patch(
  '/{portfolio_id}',
  response_model=PortfolioResponse,
  status_code=200,
  description='Update a portfolio in the database',
  response_description='Portfolio updated successfully'
)
async def update_portfolio(
  portfolio_id: str,
  portfolio_data: PortfolioUpdate,
  portfolio_service: PortfolioService = Depends(get_portfolio_service),
  current_user: UserResponse = Depends(get_current_user),
):
  user = await current_user
  try:
    return await portfolio_service.update_portfolio(
      portfolio_id,
      portfolio_data,
      user.id
    )
  except ValueError as e:
    logging.error(f'Error updating portfolio: {e}')
    raise HTTPException(status_code=400, detail=str(e))
#
@router.delete(
  '/{portfolio_id}',
  status_code=204,
  description='Delete a portfolio from the database',
  response_description='Portfolio deleted successfully'
)
async def delete_portfolio(
  portfolio_id: str,
  portfolio_service: PortfolioService = Depends(get_portfolio_service),
  current_user: UserResponse = Depends(get_current_user),
):
  user = await current_user
  try:
    await portfolio_service.delete_portfolio(portfolio_id, user.id)
  except ValueError as e:
    logging.error(f'Error deleting portfolio: {e}')
    raise HTTPException(status_code=400, detail=str(e))

@router.get(
  '/{portfolio_id}',
  response_model=PortfolioResponse,
  status_code=200,
  description='Get a portfolio by id',
  response_description='Portfolio retrieved successfully'
)
async def get_portfolio(
  portfolio_id: str,
  portfolio_service: PortfolioService = Depends(get_portfolio_service),
  current_user: UserResponse = Depends(get_current_user),
):
  user = await current_user
  try:
    return await portfolio_service.get_portfolio(portfolio_id, user.id)
  except ValueError as e:
    logging.error(f'Error getting portfolio: {e}')
    raise HTTPException(status_code=404, detail=str(e))

@router.get(
    '/{portfolio_id}/holdings',
    response_model=PortfolioHoldingsResponse,
    status_code=200,
    description='Fetch all holdings of a portfolio by id',
    response_description='Holdings retrieved successfully'
)
async def get_portfolio_holdings(
    portfolio_id: str,
    portfolio_service: PortfolioService = Depends(get_portfolio_service),
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Fetch all holdings of a specific portfolio by its ID.
    """
    user = await current_user
    try:
        holdings = await portfolio_service.fetch_portfolio_holdings(portfolio_id, user.id)
        return PortfolioHoldingsResponse(holdings=holdings)
    except ValueError as e:
        logging.error(f'Error getting portfolio holdings: {e}')
        raise HTTPException(status_code=404, detail=str(e))

@router.get(
    '/{portfolio_id}/analysis',
    response_model=PortfolioAnalysisResponse,
    status_code=200,
    description='Fetch a financial analysis of the portfolio, including total value and asset weights',
    response_description='Portfolio analysis retrieved successfully'
)
async def get_portfolio_analysis(
    portfolio_id: str,
    portfolio_service: PortfolioService = Depends(get_portfolio_service),
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Provide a financial analysis of a specific portfolio by its ID,
    including total value and asset weights.
    """
    user = await current_user
    try:
        return await portfolio_service.calculate_portfolio_analysis(portfolio_id, user.id)
    except ValueError as e:
        logging.error(f'Error getting portfolio analysis: {e}')
        raise HTTPException(status_code=404, detail=str(e))



# @router.get(
#   '/{portfolio_id}/total-value',
#   response_model=PortfolioValueResponse,
#   status_code=200,
#   description='Get total value, invested value, and return percentage of a portfolio by id',
#   response_description='Portfolio value retrieved successfully'
# )
# async def get_total_portfolio_value(
#   portfolio_id: str,
#   portfolio_service: PortfolioService = Depends(get_portfolio_service),
#   current_user: UserResponse = Depends(get_current_user),
# ):
#   user = await current_user
#   try:
#     return await portfolio_service.calculate_portfolio_value(portfolio_id, user.id)
#   except ValueError as e:
#     logging.error(f'Error getting portfolio value: {e}')
#     raise HTTPException(status_code=404, detail=str(e))
