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

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def verify_password(plain_password: str, salt: str, hashed_password: str) -> bool:
    return pwd_context.verify(salt + plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

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

def create_refresh_token(data: dict) -> str:
  """
  Create refresh token
  :param data: dict
  :rtype: str
  """
  return create_access_token(data, expires_delta = REFRESH_TOKEN_EXPIRE_DAYS)

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
  """
  Get current user id from token, if token is valid return user id
  :param token: str
  :return: str
  """
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id: str = payload.get('sub')
    if user_id is None:
      raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
  )
  except JWTError as e:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail=f'Could not validate credentials: {str(e)}',
      headers={'WWW-Authenticate': 'Bearer'},
    )

  return user_id

# Method's to check if user has roles
def check_user_roles(user: User, roles: list) -> bool:
  """
  Check if user has roles
  :param user: User
  :param roles: List
  :return: bool
  """
  pass



