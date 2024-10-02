import logging
from fastapi import (
  APIRouter,
  HTTPException,
  Depends
)
from fastapi.security import HTTPAuthorizationCredentials

# from app.core.security import get_current_user_id
from app.repository.portfolio import PortfolioRepository
from app.repository.user import UserRepository
from app.routes.auth import get_user_service

# from app.routes.auth import auth_handler
from app.schemas.portfolio import PortfolioResponse, PortfolioBase, PortfolioUpdate
from app.services.portfolio import PortfolioService, get_portfolio_service
from app.services.user import UserService
from app.utils.jwt import AuthHandler

# Inject the dependency PortfolioRepository into the PortfolioService
# def get_portfolio_service():
#   portfolio_repository = PortfolioRepository()
#   return PortfolioService(repository=portfolio_repository)

# Inject the dependency AuthHandler into the PortfolioService
def get_auth_handler(user_service: UserService = Depends(get_user_service)):
  return AuthHandler(user_service)

router = APIRouter(
  prefix='/portfolio',
  tags=['portfolio']
)

@router.get(
  '/',
  response_model=list[PortfolioResponse],
  status_code=200,
  description='Get all portfolios of the current user from the database',
  response_description='Portfolios retrieved successfully'
)
async def get_all_portfolio(
  portfolio_service: PortfolioService = Depends(get_portfolio_service),
  auth_handler: AuthHandler = Depends(get_auth_handler),
  auth: HTTPAuthorizationCredentials = Depends(get_auth_handler().security),
):
  try:
    user = await auth_handler.get_user(auth.credentials)
    return await portfolio_service.get_all_portfolio(user.id)
  except ValueError as e:
    logging.error(f"Error getting all portfolios: {e}")
    raise HTTPException(status_code=404, detail=str(e))

# @router.post(
#   '/',
#   response_model=PortfolioResponse,
#   status_code=201,
#   description='Create a new portfolio of the current user in the database',
#   response_description='Portfolio created successfully'
# )
# async def create_portfolio(
#   portfolio: PortfolioBase,
#   portfolio_service: PortfolioService = Depends(get_portfolio_service),
#   # auth_handler: AuthHandler = Depends(get_auth_handler),
#   # auth: HTTPAuthorizationCredentials = Depends(lambda: auth_handler.security),
# ):
  # try:
  #   user = await auth_handler.get_user(auth.credentials)
  #   return await portfolio_service.create_portfolio(portfolio, user.id)
  # except ValueError as e:
  #   logging.error(f'Error creating portfolio: {e}')
  #   raise HTTPException(status_code=400, detail=str(e))

# @router.patch(
#   '/{portfolio_id}',
#   response_model=PortfolioResponse,
#   status_code=200,
#   description='Update a portfolio in the database',
#   response_description='Portfolio updated successfully'
# )
# async def update_portfolio(
#   portfolio_id: str,
#   portfolio: PortfolioUpdate,
#   portfolio_service: PortfolioService = Depends(get_portfolio_service),
#   # auth_handler: AuthHandler = Depends(get_auth_handler),
#   # auth: HTTPAuthorizationCredentials = Depends(lambda: auth_handler.security),
# ):
  # user = await auth_handler.get_user(auth.credentials)
  # try:
  #   return await portfolio_service.update_portfolio(
  #     portfolio_id,
  #     portfolio,
  #     user.id
  #   )
  # except ValueError as e:
  #   logging.error(f'Error updating portfolio: {e}')
  #   raise HTTPException(status_code=400, detail=str(e))

# @router.delete(
#   '/{portfolio_id}',
#   status_code=204,
#   description='Delete a portfolio from the database',
#   response_description='Portfolio deleted successfully'
# )
# async def delete_portfolio(
#   portfolio_id: str,
#   portfolio_service: PortfolioService = Depends(get_portfolio_service),
  # auth_handler: AuthHandler = Depends(get_auth_handler),
  # auth: HTTPAuthorizationCredentials = Depends(lambda: auth_handler.security),
# ):
  # user = await auth_handler.get_user(auth.credentials)
  # try:
  #   await portfolio_service.delete_portfolio(portfolio_id, user.id)
  # except ValueError as e:
  #   logging.error(f'Error deleting portfolio: {e}')
  #   raise HTTPException(status_code=400, detail=str(e))

# @router.get(
#   '/{portfolio_id}',
#   response_model=PortfolioResponse,
#   status_code=200,
#   description='Get a portfolio by id',
#   response_description='Portfolio retrieved successfully'
# )
# async def get_portfolio(
#   portfolio_id: str,
#   portfolio_service: PortfolioService = Depends(get_portfolio_service),
#   # auth_handler: AuthHandler = Depends(get_auth_handler),
#   # auth: HTTPAuthorizationCredentials = Depends(lambda: auth_handler.security),
# ):
  # user = await auth_handler.get_user(auth.credentials)
  # try:
  #   return await portfolio_service.get_portfolio(portfolio_id, user.id)
  # except ValueError as e:
  #   logging.error(f'Error getting portfolio: {e}')
  #   raise HTTPException(status_code=404, detail=str(e))
