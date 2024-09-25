from pydantic import BaseModel

# Model for token response payload
class Token(BaseModel):
  access_token: str
  token_type: str

# Model for token data payload
class TokenData(BaseModel):
  user_id: str
  expires_at: int
