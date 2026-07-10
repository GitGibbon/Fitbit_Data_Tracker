import requests

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