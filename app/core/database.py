import os
from motor.motor_asyncio import AsyncIOMotorClient
# from pymongo.errors import ConnectionFailure

MONGO_URI = os.getenv("MONGO_URI", None)
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

def get_databse_name():
  if ENVIRONMENT == "production":
    return "app_production"
  elif ENVIRONMENT == "testing":
    return "app_testing"
  elif ENVIRONMENT == "development":
    return "app_development"
  else:
    raise ValueError(f"Unknown environment: {ENVIRONMENT}")

client = AsyncIOMotorClient(MONGO_URI)
db = client.get_database(get_databse_name())
