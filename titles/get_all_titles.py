import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import os
import json
import time

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

# Make a  request
data = []
page_n = 0

while True:
    response = oauth.get(f"{SITE}/v2/titles?page={page_n}")
    print(response)
    json_res = response.json()
    data.append(json_res)
    print(response.text)
    page_n += 1
    if len(json_res) < 30:
        break
    time.sleep(0.3)

# write to a new file, create if doesn't exist
with open("titles.json", "w+") as outfile:
    json.dump(data, outfile)
