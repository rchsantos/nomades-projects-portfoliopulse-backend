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

from app.models.user import User
from app.repository.user import UserRepository

class UserService:
  def __init__(self):
    self.repository = UserRepository()

  # Validate user data
  # check if user exists

  def get_users(self):
    pass

  def create_user(self, user: User) -> User:
    # TODO: Check if user exists
    # TODO: Salt and hash password
    # TODO: Insert user into the database
    # Business Logic Validation

    return self.repository.create_user(user)

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


