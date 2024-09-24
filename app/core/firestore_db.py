import os
import firebase_admin
from firebase_admin import credentials, firestore

CURR_DIR = os.path.dirname(__file__)

cred = credentials.Certificate(os.path.join(CURR_DIR, 'service-account-file.json'))
firebase_admin.initialize_app(cred)
db = firestore.client()
