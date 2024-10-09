from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.repository.asset import AssetRepository
from app.repository.portfolio import PortfolioRepository
from app.repository.transaction import TransactionRepository
from app.repository.user import UserRepository
from app.services.asset import AssetService
from app.services.portfolio import PortfolioService
from app.services.transaction import TransactionService
from app.services.user import UserService
from app.utils.jwt import AuthHandler

def get_user_service() -> UserService:
  user_repository = UserRepository()
  return UserService(repository=user_repository)

def get_current_user(auth: HTTPAuthorizationCredentials = Security(HTTPBearer())):
  user_service = get_user_service()
  auth_handler = AuthHandler(user_service)
  return auth_handler.get_current_user(auth)

def get_portfolio_service():
  portfolio_repository = PortfolioRepository()
  asset_repository = AssetRepository()
  return PortfolioService(portfolio_repository=portfolio_repository, asset_repository=asset_repository)

def get_asset_service():
  asset_repository = AssetRepository()
  return AssetService(repository=asset_repository)

def get_transaction_service():
  transaction_repository = TransactionRepository()
  portfolio_repository = PortfolioRepository()
  asset_repository = AssetRepository()
  portfolio_service = PortfolioService(portfolio_repository, asset_repository)
  asset_service = AssetService(asset_repository)
  return TransactionService(transaction_repository, portfolio_service, asset_service)
