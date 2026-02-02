import firebase_admin
from firebase_admin import credentials, firestore
import json
import os

# cred = credentials.ApplicationDefault()
# firebase_admin.initialize_app(cred)

if not firebase_admin._apps:
    cred_dict = json.loads(os.environ["FIREBASE_CREDENTIALS_JSON"])
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)


db = firestore.client()
