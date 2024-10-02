from fastapi import HTTPException, status, Security, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional

from app.core.config import settings
from app.models.user import blacklist_tokens
from app.schemas.user import UserResponse, UserResponseVerify
from app.services.user import UserService

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


class AuthHandler:
  """
  Auth handler class is the core of our JWT authentication system. it handles password hashing, token creation, token verification, and user authentication.
  """
  def __init__(self, user_service: UserService):
    self.user_service = user_service

  security = HTTPBearer()
  pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

  async def verify_password(self, plain_password: str, salt: str, hashed_password: str) -> bool:
    return self.pwd_context.verify(salt + plain_password, hashed_password)

  async def get_password_hash(self, password: str):
    return self.pwd_context.hash(password)

  async def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create access token
    :param data: dict
    :param expires_delta: Optional[timedelta]
    :rtype: str
    """
    to_encode = data.copy()

    if expires_delta:
      expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    else:
      expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


  async def get_user(self, username: str) -> UserResponse:
    """
    Get user by username
    :param username:
    :rtype: UserResponse
    :raises HTTPException: If user not found
    """
    user: UserResponse = await self.user_service.get_user_by_username(username)
    if not user:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found...')
    return user

  async def get_user_to_verify_login(self, username: str) -> UserResponseVerify:
    """
    Get user by username to verify login
    :param username:
    :return:
    """
    user: UserResponseVerify = await self.user_service.get_user_to_verify_login(username)
    if not user:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found...')
    return user

  async def authenticate_user(self, username: str, password: str) -> UserResponseVerify | bool:
    """
    Authenticate user
    :param username:
    :param password:
    :rtype: UserResponse or bool
    """
    user: UserResponseVerify = await self.get_user_to_verify_login(username)
    if not user:
      return False
    if not await self.verify_password(password, user.salt, user.password):
      return False
    return user

  async def blacklisted_token(self, token: str) -> None:
    """
    Blacklist token
    :param token: str
    :rtype: bool
    """
    blacklist_tokens.add(token)

  async def is_token_blacklisted(self, token: str) -> bool:
    """
    Check if token is blacklisted
    :param token: str
    :rtype: bool
    """
    return token in blacklist_tokens

  async def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)) -> UserResponse:
    """
    Auth wrapper
    :param auth: HTTPAuthorizationCredentials
    :rtype: UserResponse
    """
    token = auth.credentials
    if not token or await self.is_token_blacklisted(token):
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Not authenticated',
        headers={'WWW-Authenticate': 'Bearer'}
        )
    try:
      payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
      username: str = payload.get('sub')
      if username is None:
        raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail='Could not validate credentials',
          headers={'WWW-Authenticate': 'Bearer'}
        )
    except JWTError as e:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f'Could not validate credentials: {str(e)}',
        headers={'WWW-Authenticate': 'Bearer'}
      )

    user = await self.get_user(username)
    if not user:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='User not found',
        headers={'WWW-Authenticate': 'Bearer'}
      )
    return user

  async def get_current_user(self, auth: HTTPAuthorizationCredentials = Security(security)) -> UserResponse:
    """
    Get current user
    :param auth: HTTPAuthorizationCredentials
    :rtype: UserResponse
    """
    return await self.auth_wrapper(auth)

# def get_auth_handler(user_service: UserService = Depends(get_user_service())):
#   return AuthHandler(user_service)
