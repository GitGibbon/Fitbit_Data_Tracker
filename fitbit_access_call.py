import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("GOOGLE_CLIENT_ID")
client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
refresh_token = os.getenv("GOOGLE_REFRESH_TOKEN")

def refresh_access_token(refresh_token, client_id, client_secret):
    token_url = "https://oauth2.googleapis.com/token"

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret  
        }

    response = requests.post(token_url, data=data).json()
    return response.get("access_token")

access_token = refresh_access_token(refresh_token, client_id, client_secret)