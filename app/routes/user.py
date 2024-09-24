from fastapi import (
  APIRouter,
  status,
  HTTPException,
  Depends
)

from app.models.user import User
from app.repository.user import UserRepository
from app.services.user import UserService
from app.schemas.user import UserCreate, UserResponse

# Inject the dependency UserRepository into the UserService
def get_user_service():
  user_repository = UserRepository()
  return UserService(repository=user_repository)

router = APIRouter(prefix='/user', tags=['users'])

@router.get(
  '/',
  response_model=list[UserResponse],
  status_code=status.HTTP_200_OK,
  description='Get all users from the database',
  response_description='List of all users'
)
async def get_all_users(user_service: UserService = Depends(get_user_service)):
  try:
    return user_service.get_all_users()
  except ValueError as e:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

# Create a new user and return the new user
@router.post(
  '/',
  response_model=UserResponse,
  status_code=status.HTTP_201_CREATED,
  description='Create a new user in the database',
  response_description='User created successfully'
)
async def create_user(user: UserCreate, user_service: UserService = Depends(get_user_service)):
  try:
    return user_service.create_user(user)
  except ValueError as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# Update a user
@router.put('/{user_id}')
async def update_user():
    return {"message": "Update a user"}

# Delete a user
@router.delete('/{user_id}')
async def delete_user():
    return {"message": "Delete a user"}


# Get a user by id
async def get_user_by_id():
    return {"message": "Get a user by id"}


# Get a user by email
async def get_user_by_email():
    return {"message": "Get a user by email"}


# Get a user by username
async def get_user_by_username():
    return {"message": "Get a user by username"}


# Route /me
async def get_user_me():
        return {"message": "Get me"}

