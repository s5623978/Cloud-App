from firebase_admin import auth
import dotenv
import os
import requests

dotenv.load_dotenv()

FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")
BASE_URL = "https://identitytoolkit.googleapis.com/v1"

def login_user(email, password):
    url = f"{BASE_URL}/accounts:signInWithPassword?key={FIREBASE_API_KEY}"

    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def create_user(email, password):
    response = auth.create_user(
        email=email,
        password=password
    )

    if response is not None:
        return response
    else:
        return None
    
def logout(request):
    try:
        del request.session['user']
    except KeyError:
        pass