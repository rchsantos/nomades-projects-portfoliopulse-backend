import logging
from fastapi import (
  APIRouter,
  status,
  HTTPException,
  Depends
)
from sqlalchemy.sql.functions import current_user

from app.services.user import UserService
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.dependencies import get_user_service, get_current_user



router = APIRouter(
  prefix='/user',
  tags=['users']
)

@router.get(
  '/',
  response_model=list[UserResponse],
  status_code=status.HTTP_200_OK,
  description='Get all users from the database',
  response_description='List of all users'
)
async def get_all_users(
  user_service: UserService = Depends(get_user_service),
  current_user: UserResponse = Depends(get_current_user)
):
  try:
    return await user_service.get_all_users()
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
async def create_user(
  user: UserCreate,
  user_service: UserService = Depends(get_user_service)):
  try:
    return await user_service.create_user(user)
  except ValueError as e:
    logging.error(f'Error creating user: {e}')
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Update a user
@router.patch(
  '/{user_id}',
  response_model=UserResponse,
  status_code=status.HTTP_200_OK,
  description='Update a user in the database',
  response_description='User updated successfully',
)
async def update_user(
  user_id: str ,
  user_data: UserUpdate,
  user_service: UserService = Depends(get_user_service),
  current_user: UserResponse = Depends(get_current_user)
):
  try:
    return await user_service.update_user(user_id, user_data.model_dump(exclude_unset=True))
  except ValueError as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Delete a user
@router.delete(
  '/{user_id}',
  status_code=status.HTTP_200_OK,
  description='Delete a user from the database',
  response_description='User deleted successfully'
)
async def delete_user(
  user_id: str,
  user_service: UserService = Depends(get_user_service),
  current_user: UserResponse = Depends(get_current_user)
):
  try:
    await user_service.delete_user(user_id)
  except ValueError as e:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
  return {"message": 'User deleted successfully'}
