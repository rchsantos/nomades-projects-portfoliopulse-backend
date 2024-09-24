"""
    This is a simple service that will simulate a user service.
    The service will have the following methods:
    - get_users: Get all users
    - create_user: Create a new user
    - update_user: Update a user
    - delete_user: Delete a user
    - get_user_by_id: Get a user by id
    - get_user_by_email: Get a user by email
    - get_user_by_username: Get a user by username
    - get_user_me: Get the current user
"""

import uuid
from passlib.context import CryptContext

from app.models.user import User
from app.repository.user import UserRepository
from app.schemas.user import UserCreate, UserResponse

class UserService:
  """
    A class to represent a user service, and contains
    all logic to interact with the repository.
  """

  def __init__(self, repository: UserRepository):
    self.repository = repository
    self.pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

  # Generate Salt
  def generate_salt(self) -> str:
    return uuid.uuid4().hex

  # Hash Password
  def hash_password(self, password: str, salt: str) -> str:
    return self.pwd_context.hash(salt + password)

  # TODO: Validate user data
  # TODO: check if user exists

  def get_all_users(self) -> list[User]:
    """
    Get all users from the database
    :return: list[User]
    :rtype: list
    :raises ValueError: If no users are found
    :raises Exception: If an error occurs
    """
    return self.repository.get_all_users()

  def create_user(self, user_data: UserCreate) -> UserResponse:
    """
    Create a new user in the database
    :param user_data:
    :type user_data: UserCreate
    :return: UserResponse
    """
    # Check if user already exists
    if self.repository.get_user_by_email(user_data.email):
      raise ValueError('User already exists')

    # Generate Salt & Hash Password
    salt = self.generate_salt()
    hashed_password = self.hash_password(user_data.password, salt)

    # Create User Object
    user = User(
      username=user_data.username,
      email=user_data.email,
      password=hashed_password,
      salt=salt,
      full_name=user_data.full_name,
      role=user_data.role,
      is_active=user_data.is_active
    )

    # Add User to Repository
    self.repository.add_user(user)

    return UserResponse(**user.model_dump())

  # def create_user(self, user: User) -> User:
  #   # Data Validation
  #   if not user.email or not user.password:
  #     raise ValueError('Email and password are required')
  #
  #   # Check if user already exists
  #   if self.repository.get_user_by_email(user.email):
  #     raise ValueError('User already exists')
  #
  #   return self.repository.add_user(user)

  def update_user(self):
    pass

  def delete_user(self):
    pass

  def get_user_by_id(self):
    pass

  def get_user_by_email(self):
    pass

  def get_user_by_username(self):
    pass

  def get_user_me(self):
    pass


