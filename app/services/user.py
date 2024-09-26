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

from app.models.user import User, UserUpdate
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
  @staticmethod
  def generate_salt() -> str:
    return str(uuid.uuid4())

  # Hash Password
  def hash_password(self, password: str, salt: str) -> str:
    return self.pwd_context.hash(salt + password)

  # TODO: Validate user data
  # TODO: check if user exists

  def get_all_users(self) -> list[UserResponse]:
    """
    Get all users from the database
    :return: list[UserResponse]
    :rtype: list
    :raises ValueError: If no users are found
    :raises Exception: If an error occurs
    """
    users = self.repository.get_all_users()
    if users:
      return [UserResponse(**user.model_dump()) for user in users]
    raise ValueError('No users found')

  def create_user(self, user_data: UserCreate) -> UserResponse:
    """
    Create a new user in the database
    :param user_data:
    :type user_data: User
    :return: UserResponse
    """
    # Check if user already exists
    if self.repository.find_user_by_email(user_data.email):
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

  def update_user(self, user_id: str, user_data: dict) -> UserResponse:
    """
    Update a user in the database
    :param user_id: str
    :param user_data: dict
    :return: UserResponse
    :raises ValueError: If user not found
    """
    user: UserUpdate = self.repository.find_user_by_id(user_id)
    if not user:
      raise ValueError('User not found')

    # If password is provided, hash it
    if 'password' in user_data:
      salt = self.generate_salt()
      hashed_password = self.hash_password(user_data['password'], salt)
      user_data['salt'] = salt
      user_data['password'] = hashed_password

    # Update all field values in the user object
    for key, value in user_data.items():
      if key != 'password':
        setattr(user, key, value)

    # Update user in the repository
    self.repository.update_user(user_id, user)

    return UserResponse(**user.model_dump())

  def delete_user(self, user_id: str) -> None:
    # Check if user exists
    user = self.repository.find_user_by_id(user_id)
    if not user:
      raise ValueError('User not found')

    # Delete user from the repository
    self.repository.delete_user(user_id)

  def get_user_me(self):
    pass


