from fastapi import (
  APIRouter,
  Depends,
  HTTPException,
  status
)

from app.core.security import create_access_token
from app.repository.user import UserRepository
from app.routes.user import create_user
from app.schemas.auth import RegisterResponse, LoginResponse, LoginRequest
from app.services.authentication import Authentication

router = APIRouter()

# Inject the dependency user repository
def get_user_repository():
  return UserRepository()

def get_authentication_service(user_repo: UserRepository = Depends(get_user_repository)):
  return Authentication(user_repo)

@router.post(
  '/register',
  response_model=RegisterResponse,
  status_code=status.HTTP_201_CREATED,
  description='Register a new user',
  response_description='User registered successfully'
)
async def register_user(
  user: RegisterResponse,
  user_repo: UserRepository = Depends(get_user_repository)
):
  return await create_user(user, user_repo)

@router.post(
  '/login',
  response_model=LoginResponse,
  status_code=status.HTTP_200_OK,
  description='Authenticate a user and return an access token.',
  response_description='Access token and token type'
)
async def login(
  login_request: LoginRequest,
  auth_service: Authentication = Depends(get_authentication_service)
):
  user = auth_service.authenticate_user(login_request.email, login_request.password)
  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail='Invalid authentication credentials',
      headers={'WWW-Authenticate': 'Bearer'}
    )

  access_token = create_access_token({'sub': user.email})
  return {
    'access_token': access_token,
    'token_type': 'bearer'
  }

