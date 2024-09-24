from typing import Optional
from uuid import UUID
from app.core.firestore_db import db

from app.models.user import User
import app.schemas.user as user_schema

class UserRepository:
  """
    A class to represent a user repository, and contains
    methods to interact with the database.
  """

  def __init__(self) -> None:
    self.collection = db.collection(u'users')
    self.user_schema = user_schema

  def get_all_users(self) -> list[User]:
    """
    Get all users from the database
    :return: list[User]
    :rtype list
    """
    return [User(**user.to_dict()) for user in self.collection.get()]

  def add_user(self, user: User) -> None:
    """
    Add a new user to the database
    :param user:
    :return: None
    """
    try:
      self.collection.add(self.user_to_firestore(user))
    except Exception as e:
      raise ValueError (str(e))

  def update_user(self, user: User) -> User:
    """
    Update a user in the database
    :param user:
    :return: User
    """
    try:
      self.collection.document(str(user.id)).update(self.user_to_firestore(user))
      return user
    except Exception as e:
      raise ValueError(str(e))

  def delete_user(self, user_id: UUID) -> None:
    """
    Delete a user from the database
    :param user_id:
    :return: None
    """
    try:
      self.collection.document(str(user_id)).delete()
    except Exception as e:
      raise ValueError(str(e))

  def find_user_by_id(self, user_id: UUID) -> Optional[User]:
    user = self.collection.document(str(user_id)).get()
    if user.exists:
      return User(**user.to_dict())
    return None

  def find_user_by_email(self, email: str) -> bool:
    user = self.collection.where(
      u'email', u'==', email
    ).get()
    if user:
      return True
    return False

  # Transform a user object to a dictionary for storage in firestore
  def user_to_firestore(self, user: User) -> dict:
    return {
      u'id': user.id,
      u'username': user.username,
      u'email': user.email,
      u'password': user.password,
      u'salt': user.salt,
      u'full_name': user.full_name,
      u'role': user.role,
      u'is_active': user.is_active
    }
