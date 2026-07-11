import requests

def refresh_access_token(refresh_token, client_id, client_secret):
    token_url = "https://oauth2.googleapis.com/token"

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret  
        }
    try:
        ask = requests.post(token_url, data=data, timeout=10) #timeout is in seconds, token_url is the url we are sending to (endpoint), and data=data is the data we are sending.
        ask.raise_for_status()
    except requests.exceptions.HTTPError:
        raise RuntimeError(f"HTTP error occurred: {ask.status_code} - {ask.text}")
    response = ask.json()
    return response.get("access_token")