from typing import Optional

from google.cloud.firestore_v1 import DocumentSnapshot, FieldFilter

from app.core.firestore_db import db

from app.models.user import User, UserUpdate
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

  def add_user(self, user: User) -> User:
    """
    Add a new user to the database
    :param user:
    :return: None
    """
    try:
      _, user_ref = self.collection.add(self.user_to_firestore(user))
      user.id = user_ref.id
      return user
    except Exception as e:
      raise ValueError (str(e))

  def update_user(
    self,
    user_id: str,
    user: UserUpdate) -> UserUpdate:
    """
    Update a user in the database
    :param user_id:
    :param user:
    :return: User
    """
    try:
      self.collection.document(user_id).update(self.user_to_firestore(user))
      return user
    except Exception as e:
      raise ValueError(str(e))

  def delete_user(self, user_id: str) -> None:
    """
    Delete a user from the database
    :param user_id: str
    :return: None
    :raises ValueError: If an error occurs
    """
    try:
      self.collection.document(user_id).delete()
    except Exception as e:
      raise ValueError(str(e))

  def find_user_by_id(self, user_id: str) -> Optional[User]:
    user = self.collection.document(user_id).get()
    if user.exists:
      return User(**user.to_dict())
    return None

  def find_user_by_email(self, email: str) -> Optional[User] | None:
    user = self.collection.where(
      filter=FieldFilter(u'email', u'==', email)
    ).get()
    if user:
      return self.firestore_to_user(user[0])
    return None

  # Transform a user object to a dictionary for storage in firestore
  @staticmethod
  def user_to_firestore(user: User|UserUpdate ) -> dict:
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

  # Transform a firestore document to a user object
  @staticmethod
  def firestore_to_user(user_document: DocumentSnapshot) -> User:
    user_data = user_document.to_dict()
    return User(
      id = user_document.id,
      username = user_data['username'],
      email = user_data['email'],
      password = user_data['password'],
      salt = user_data['salt'],
      full_name = user_data['full_name'],
      role = user_data['role'],
      is_active = user_data.get('is_active', True)
    )
