from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.repository.user import UserRepository
from app.services.user import UserService
from app.utils.jwt import AuthHandler


def get_user_service() -> UserService:
  user_repository = UserRepository()
  return UserService(repository=user_repository)

def get_current_user(auth: HTTPAuthorizationCredentials = Security(HTTPBearer())):
  user_service = get_user_service()
  auth_handler = AuthHandler(user_service)
  return auth_handler.get_current_user(auth)
