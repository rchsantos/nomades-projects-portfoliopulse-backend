from datetime import timedelta
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from app.models.auth import TokenResponse
from app.schemas.auth import LoginRequest, RegisterResponse
from app.schemas.user import UserCreate, UserResponseVerify
from app.services.user import UserService
from app.utils.jwt import AuthHandler, ACCESS_TOKEN_EXPIRE_MINUTES


class AuthService:
  def __init__(
    self,
    user_service: UserService,
    auth_handler: AuthHandler
  ):
    self.user_service = user_service
    self.auth_handler = auth_handler

  async def register(
    self,
    user_data: UserCreate
  ) -> RegisterResponse:
    """
    Register a new user
    :param user_data: UserCreate
    :return: dict[RegisterResponse]
    """
    try:
      user = await self.user_service.create_user(user_data)
      return RegisterResponse(**user.model_dump())
    except Exception as e:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(e)
      )

  async def login(
    self,
    login_request: LoginRequest
  ) -> TokenResponse:
    """
    Authenticate a user and return an access token
    :param login_request: LoginRequest
    :rtype: TokenResponse
    """
    user: UserResponseVerify = await self.auth_handler.authenticate_user(login_request.username, login_request.password)
    if not user:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid authentication credentials',
        headers={'WWW-Authenticate': 'Bearer'}
      )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await self.auth_handler.create_access_token(
      data={'sub': user.username},
      expires_delta=access_token_expires
    )

    return TokenResponse(
      access_token=access_token,
      token_type='bearer'
    )

  async def logout(
    self,
    auth: HTTPAuthorizationCredentials
  ) -> dict:
    """
    Log out a user
    :param auth: HTTPAuthorizationCredentials
    :return: dict
    """
    await self.auth_handler.blacklisted_token(auth.credentials)
    return {'message': 'User logged out successfully'}
