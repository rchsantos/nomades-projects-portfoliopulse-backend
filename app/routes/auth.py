from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import HTTPAuthorizationCredentials
from app.schemas.auth import RegisterResponse, LoginRequest, LoginResponse
from app.schemas.user import UserCreate
from app.services.user import UserService
from app.services.auth import AuthService
from app.utils.jwt import AuthHandler
from app.repository.user import UserRepository


router = APIRouter()


def get_user_repository():
  return UserRepository()


def get_user_service(user_repo: UserRepository = Depends(get_user_repository)):
  return UserService(user_repo)


def get_auth_handler(user_service: UserService = Depends(get_user_service)):
  return AuthHandler(user_service)


def get_auth_service(
  user_service: UserService = Depends(get_user_service),
  auth_handler: AuthHandler = Depends(get_auth_handler)
):
  return AuthService(user_service, auth_handler)

@router.post(
    '/register',
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    description='Register a new user',
    response_description='User registered successfully'
)
async def register_user(
    user: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
):
    return await auth_service.register(user)


@router.post(
    '/login',
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    description='Authenticate a user and return an access token.',
    response_description='Access token and token type'
)
async def login(
    login_request: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    return await auth_service.login(login_request)

@router.post(
    '/logout',
    status_code=status.HTTP_200_OK,
    description='Logout a user',
    response_description='User logged out successfully'
)
async def logout(
    auth: HTTPAuthorizationCredentials = Security(get_auth_handler().security),
    auth_handler: AuthHandler = Depends(get_auth_handler)
):
    await auth_handler.blacklisted_token(auth.credentials)
    return {
        'message': 'Logged out successfully'
    }

# TODO: Create a Forgot Password endpoint
