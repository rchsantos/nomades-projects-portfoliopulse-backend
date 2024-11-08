from typing import Optional
from bson import ObjectId

from app.core.database import db

from app.models.user import User, UserUpdate
import app.schemas.user as user_schema

class UserRepository:
  """
    A class to represent a user repository, and contains
    methods to interact with the database.
  """
  def __init__(self) -> None:
    self.collection = db.get_collection('users')
    self.user_schema = user_schema

  async def fetch_users(self) -> list[User]:
    """
    Fetch all users from the database
    :rtype list[User]
    """
    user_cursor = self.collection.find()
    users = []
    async for user in user_cursor:
      user['id'] = str(user['_id'])
      users.append(User(**user))
    return users

  async def insert_user(self, user: User) -> User:
    """
    Add a new user to the database
    :param user: User
    :rtype: User
    :raises ValueError: If an error occurs
    """
    try:
      user_dict = user.model_dump()
      return await self.collection.insert_one(user_dict)
    except Exception as e:
      raise ValueError (str(e))

  async def update_user(
    self,
    user_id: str,
    user: dict) -> User:
    """
    Update a user in the database
    :param user_id: str
    :param user: UserUpdate
    :rtype: UserUpdate
    """
    try:
      await self.collection.update_one(
        {'_id': ObjectId(user_id)},
        {
          '$set': user,
          '$currentDate': {'lastUpdated': True}
        }
      )
      update_user = await self.collection.find_one({'_id': ObjectId(user_id)})
      return update_user
    except Exception as e:
      raise ValueError(str(e))

  async def delete_user(self, user_id: str) -> None:
    """
    Delete a user from the database
    :param user_id: str
    :rtype: None
    :raises ValueError: If an error occurs
    """
    try:
      self.collection.delete_one({'_id': ObjectId(user_id)})
    except Exception as e:
      raise ValueError(str(e))

  async def find_user_by_email(self, email: str) -> Optional[User]:
    """
    Find a user by email
    :param email:
    :rtype: Optional[User]
    """
    return await self.collection.find_one({'email': email})

  async def find_user_by_id(self, user_id: str) -> Optional[User]:
    """
    Find a user by id
    :param user_id:
    :rtype: Optional[User]
    """
    user = await self.collection.find_one({'_id': ObjectId(user_id)})
    return user

  async def find_user_by_username(self, username: str) -> Optional[User]:
    """
    Find a user by username
    :param username:
    :rtype: Optional[User]
    """
    user = await self.collection.find_one({'username': username})
    return user
