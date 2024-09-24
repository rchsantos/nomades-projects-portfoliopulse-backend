from fastapi import (
  APIRouter,
  status,
  HTTPException
)

from app.models.user import User, UserResponse
from app.services.user import UserService

router = APIRouter(prefix='/user', tags=['users'])

# Get all users and return a list of users
@router.get('/')
async def get_users():
    return {"message": "Get all users"}

# Create a new user and return the new user
@router.post('/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
  user_model_dump = user.model_dump()
  try:
    return UserService().create_user(User(**user_model_dump))
  except Exception as e:
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

