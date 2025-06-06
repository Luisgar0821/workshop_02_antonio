import requests
import base64


client_id = "a4463cb99d6d458f95655ffd5ef4ea22"
client_secret = "9aff2a4d8adf44948e94b97b31215bb0"

def get_token(client_id, client_secret):
    auth_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post(auth_url, headers=headers, data=data)

    if response.status_code == 200:
        token = response.json().get("access_token")
        print("✅ Token obtenido exitosamente:")
        print(token)
        return token
    else:
        print(f"❌ Error {response.status_code}:")
        print(response.json())
        return None

if __name__ == "__main__":
    get_token(client_id, client_secret)


