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

class UserService:
  def __init__(self):
    self.repository = UserRepository()

  # TODO: Validate user data
  # TODO: check if user exists

  def get_users(self):
    pass

  def create_user(self, user: User) -> User:
    # Data Validation
    if not user.email or not user.password:
      raise ValueError('Email and password are required')

    # Check if user already exists
    if self.repository.get_user_by_email(user.email):
      raise ValueError('User already exists')

    # Salt and hash password
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    salt = uuid.uuid4().hex
    user.salt = salt
    user.password = pwd_context.hash(user.salt + user.password)

    return self.repository.add_user(user)

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


