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

  # def get_all_users(self) -> list[User]:
  #   """
  #   Get all users from the database
  #   :return: list[User]
  #   :rtype: list
  #   :raises ValueError: If no users are found
  #   :raises Exception: If an error occurs
  #   """
  #   try:
  #     users = self.collection.get()
  #     if users:
  #       return [self.user_schema.to_user(user) for user in users]
  #   except Exception as e:
  #     raise ValueError(str(e))
  #   raise ValueError('No users found')

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

  def get_user_by_email(self, email: str) -> bool:
    user = self.collection.where(
      u'email', u'==', email
    ).get()
    if user:
      return True
    return False

  # Transform a user object to a dictionary for storage in firestore
  def user_to_firestore(self, user: User) -> dict:
    return {
      u'username': user.username,
      u'email': user.email,
      u'password': user.password,
      u'salt': user.salt,
      u'full_name': user.full_name,
      u'role': user.role,
      u'is_active': user.is_active
    }
