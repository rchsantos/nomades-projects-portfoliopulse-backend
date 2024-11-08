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
    TODO: Implement the user can manage their own account
"""
import uuid

from passlib.context import CryptContext
from app.models.user import User, UserUpdate
from app.repository.user import UserRepository
from app.schemas.user import UserCreate, UserResponseVerify, UserBase, UserResponse

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

  async def get_all_users(self) -> list[UserResponse]:
    """
    Get all users from the database
    :return: list[UserResponse]
    :rtype: list
    :raises ValueError: If no users are found
    :raises Exception: If an error occurs
    """
    users: list[User] = await self.repository.fetch_users()
    if users:
      return [UserResponse(**user.model_dump()) for user in users]
    raise ValueError('No users found')

  async def create_user(self, user_data: UserCreate) -> UserResponse:
    """
    Create a new user in the database
    :param user_data:
    :type user_data: User
    :return: UserResponse
    """
    # Check if user already exists by email
    existing_user = await self.repository.find_user_by_email(user_data.email)
    if existing_user:
      raise ValueError('User withing email already exists')

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
    result = await self.repository.insert_user(user)
    user.id = str(result.inserted_id)
    return UserResponse(**user.model_dump())

  async def update_user(self, user_id: str, user_data: UserUpdate) -> UserResponse:
    """
    Update a user in the database
    :param user_id: str
    :param user_data: dict
    :return: UserResponse
    :raises ValueError: If user not found
    """
    user = await self.repository.find_user_by_id(user_id)
    if not user:
      raise ValueError('User not found')

    user_dic = user_data.model_dump(exclude_unset=True)

    # If password is provided, hash it
    if user_data.password:
      salt = self.generate_salt()
      hashed_password = self.hash_password(user_data.password, salt)
      user_dic['salt'] = salt
      user_dic['password'] = hashed_password

    updated_user = await self.repository.update_user(user_id, user_dic)
    updated_user['id'] = user_id
    return UserResponse(**updated_user)

  async def delete_user(self, user_id: str) -> None:
    """
    Delete a user from the database
    :param user_id: str
    :return: None
    :raises ValueError: If user not found
    """
    # Check if user exists
    user: User = await self.repository.find_user_by_id(user_id)
    if not user:
      raise ValueError('User not found')

    # Delete user from the repository
    await self.repository.delete_user(user_id)

  # async def get_user_by_email(self, email: str) -> UserResponse:
  #   """
  #   Get a user by email
  #   :param email: str
  #   :return: UserResponse
  #   :raises ValueError: If user not found
  #   """
  #   user: User = self.repository.find_user_by_email(email)
  #   if user:
  #     return UserResponse(**user.model_dump())
  #   raise ValueError('User not found')

  # async def get_user_by_username(self, username: str) -> UserResponse:
  #   """
  #   Get a user by username
  #   :param username: str
  #   :rtype: UserResponse
  #   :raises ValueError: If user not found
  #   """
  #   user: User = self.repository.find_user_by_username(username)
  #   if user:
  #     return UserResponse(**user.model_dump())
  #   raise ValueError('User not found')

  async def get_user_to_verify_login(self, username: str) -> UserResponseVerify:
    """
    Get a user by username to verify login
    :param username: str
    :rtype: UserResponse
    :raises ValueError: If user not found
    """
    user: User = await self.repository.find_user_by_username(username)
    if user:
      return UserResponseVerify(**user)
    raise ValueError('User not found')

  # def get_user_me(self):
  #   pass


