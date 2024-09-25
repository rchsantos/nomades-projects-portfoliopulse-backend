import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
  SECRET_KEY = os.getenv('SECRET_KEY', 'secret')
  ALGORITHM = "HS256"
  ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN', 30))


settings = Settings()
