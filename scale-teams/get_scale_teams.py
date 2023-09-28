import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import os
import json
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

user_id = 111878

# Make a GET request
response = oauth.get(f"{SITE}/v2/users/{user_id}/scale_teams?filter[future]=true")

res = response.json()

for r in res:
    print(r['id'])
    print(r['feedback'])
    print(r['final_mark'])
# Print response status and content
# print(response.status_code)
# print(response.text)
