from typing import Optional

from app.core.security import verify_password
from app.models.user import User
from app.repository.user import UserRepository

class Authentication:
  def __init__(self,user_repository: UserRepository):
    self.user_repository = user_repository

  def authenticate_user(self,email: str, password: str) -> Optional[User] | None:
    """
      Authenticate user
      :param email: str
      :param password: str
      :return: Optional[User]
      :rtype: Optional[User]
      """
    user = self.user_repository.find_user_by_email(email)
    if not user or not verify_password(password, user.salt, user.password):
      return None

    return user
