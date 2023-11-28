import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import os
import time
import colorama
from colorama import Fore, Back, Style

colorama.init(autoreset=True)

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

# Fetch the token using client_credentials flow
token = oauth.fetch_token(
    token_url=f"{SITE}/oauth/token", client_id=UID, client_secret=SECRET, scope=SCOPE
)


# Can be negative to remove correction points

# Who to airdrop
user_ids = [
    "wikee",
]


# Field needed by intra
reason = "reset to 5"
RESET_TO = 5
# Build payload
payload = {"reason": reason, "amount": 0}

for user_id in user_ids:
    # Make request
    response = oauth.get(f"{SITE}/v2/users/{user_id}")
    correction_points = int(response.json()['correction_point'])
    diff = (RESET_TO - correction_points) if (correction_points < RESET_TO) else ((correction_points * -1) + RESET_TO)
    print(f"{user_id} had {correction_points} points, requested to add {diff}")
    payload['amount'] = diff
    response = oauth.post(
        f"{SITE}/v2/users/{user_id}/correction_points/add", json=payload
    )

    # Print response status and content
    color = Fore.GREEN
    if int(response.status_code) != 200:
        color = Fore.RED
    print(f"{color} {user_id} {response.status_code} {response.text}")
    # Wait 1 seconds to not get ratelimited, 2 requests / second
    time.sleep(1)
