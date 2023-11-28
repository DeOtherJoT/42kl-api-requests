import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import os
import time
from colorama import Fore, Back, Style

load_dotenv()

UID = os.getenv("42-UID")  # EDIT .env file
SECRET = os.getenv("42-SECRET")  # EDIT .env file

if UID == None:
    raise (Exception("UID not defined, edit .env file"))
if SECRET == None:
    raise (Exception("UID not defined, edit .env file"))

SITE = "https://api.intra.42.fr"
SCOPE = "public projects"

# Create a client using the OAuth2Session with a BackendApplicationClient
client = BackendApplicationClient(client_id=UID)
oauth = OAuth2Session(client=client)
print(SECRET)
# Fetch the token using client_credentials flow
token = oauth.fetch_token(
    token_url=f"{SITE}/oauth/token", client_id=UID, client_secret=SECRET, scope=SCOPE
)

user_ids = ["aawgku-o", "lchee-ti"]
payload = {"duration": 5, "reason": "game jam"}
# Make a request

for user_id in user_ids:
    response = oauth.post(f"{SITE}/v2/users/{user_id}/free_past_agu", json=payload)
    color = Fore.GREEN
    if int(response.status_code) != 200:
        color = Fore.RED
    print(f"{color} {user_id} {response.status_code} {response.text}")
    # Wait 0.5 seconds to not get ratelimited
    time.sleep(0.5)
