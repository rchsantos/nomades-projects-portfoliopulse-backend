"""
Authentication and Authorization System security
- verify_password: Verify password
- get_password_hash: Get password hash
- authenticate_user: Authenticate user
- create_access_token: Create access token
- get_current_user: Get current user
"""
from uuid import UUID
from datetime import datetime, timedelta, timezone
from typing import Optional
from passlib.context import CryptContext

from fastapi import (
    Depends,
    HTTPException,
    status
)
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.core.config import settings
from app.models.user import User
from app.repository.user import UserRepository

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

# Method's to authenticate user
def verify_password(plain_password: str, salt: str, hashed_password: str) -> bool:
    return pwd_context.verify(salt + plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

# def authenticate_user(
#   email: str,
#   password: str,
#   user_repo: UserRepository
# ) -> Optional[User]:
#   """
#   Authenticate user
#   :param email: str
#   :param password: str
#   :param user_repo: UserRepository
#   :return: Optional[User]
#   """
#   user = user_repo.find_user_by_email(email)
#   if not user or not verify_password(password, user.hashed_password):
#     return None
#   return user

def create_access_token(
  data: dict,
  expires_delta: Optional[int] = None
) -> str:
  """
  Create access token
  :param data: dict
  :param expires_delta: Optional[int]
  :rtype: str
  """
  to_encode = data.copy()
  expires = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
  to_encode.update({'exp': expires})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

def get_current_user(
  token: str  = Depends(oauth2_scheme),
  user_repo: UserRepository = Depends()
) -> User:
  """
  Get the current user from the token
  :param token: str
  :param user_repo: UserRepository
  :return: User
  """
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'}
  )
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id: str = payload.get('sub')
    if user_id is None:
      raise credentials_exception
  except JWTError:
    raise credentials_exception

  user = user_repo.find_user_by_id(UUID(user_id))
  if user is None:
    raise credentials_exception

  return user
