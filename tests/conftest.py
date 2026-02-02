import os
import firebase_admin
import firebase_admin.firestore
from unittest.mock import MagicMock

# Prevent Firebase from initializing during tests
firebase_admin._apps = [True]

# Mock firestore.client to return a mock db
firebase_admin.firestore.client = MagicMock(return_value=MagicMock())

def pytest_configure():
    os.environ["FIREBASE_CREDENTIALS_JSON"] = '''{
      "type": "service_account",
      "project_id": "dummy-project",
      "private_key_id": "dummy-key-id",
      "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...\n-----END PRIVATE KEY-----\n",
      "client_email": "dummy@dummy-project.iam.gserviceaccount.com",
      "client_id": "123456789",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/dummy%40dummy-project.iam.gserviceaccount.com"
    }'''
    os.environ["FIREBASE_API_KEY"] = "dummy_key"
    os.environ["DJANGO_SETTINGS_MODULE"] = "gamestore.store.settings"