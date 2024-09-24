from app.core.firestore_db import db

from app.models.user import User
import app.schemas.user as user_schema

class UserRepository:

  def __init__(self) -> None:
    self.collection = db.collection(u"users")
    self.user_schema = user_schema

  def add_user(self, user: User) -> User:
    _, user_ref = self.collection.add(self.user_schema.to_firebase_user(user))
    user.id = user_ref.id
    return user

  def get_user_by_email(self, email: str) -> User | None:
    user = self.collection.where(
      u'email', u'==', email
    ).get()
    if user:
      return self.user_schema.to_user(user[0])
    return None
