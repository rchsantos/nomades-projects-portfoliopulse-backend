from app.core.firestore_db import db

from app.models.user import User
import app.schemas.user as user_schema

class UserRepository:
  """
    A class to represent a user repository, and contains
    methods to interact with the database.
  """

  def __init__(self) -> None:
    self.collection = db.collection(u"users")
    self.user_schema = user_schema

  def get_all_users(self) -> list[User]:
    """
    Get all users from the database
    :return: list[User]
    :rtype: list
    :raises ValueError: If no users are found
    :raises Exception: If an error occurs
    """
    try:
      users = self.collection.get()
      if users:
        return [self.user_schema.to_user(user) for user in users]
    except Exception as e:
      raise ValueError(str(e))
    raise ValueError('No users found')

  def add_user(self, user: User) -> User:
    _, user_ref = self.collection.add(self.user_schema.to_firebase_user(user))
    user.id = user_ref.id
    return user

  def get_user_by_email(self, email: str) -> bool:
    user = self.collection.where(
      u'email', u'==', email
    ).get()
    if user:
      return True
    return False
