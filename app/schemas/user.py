from marshmallow import Schema, fields
from firebase_admin.firestore import DocumentSnapshot, DocumentReference
from app.models.user import User

def to_user(user: dict | DocumentSnapshot) -> User:
  user_dict = {}
  if isinstance(user, DocumentReference):
    user_dict.update({'id': user.id})
    user = user.get().to_dict()
  elif isinstance(user, DocumentSnapshot):
    user_dict.update({'id': user.id})
    user = user.to_dict()

  user_dict.update(user)
  return User(**user_dict)

def to_firebase_user(user: User) -> dict:
    return {
      u"username": user.username,
      u"email": user.email,
      u"password": user.password,
      u"full_name": user.full_name,
      u"role": user.role,
      u"is_active": user.is_active,
    }
