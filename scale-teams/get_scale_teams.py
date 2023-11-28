import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import os
import json
import pytz
from datetime import datetime
from datetime import datetime
from dateutil import tz

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

user_id = "rsoo"

# Make a GET request
response = oauth.get(
    f"{SITE}/v2/users/{user_id}/scale_teams?filter[filled]=false&range[begin_at]=2023-09-2T00:00:00.989Z,2024-09-25T13:54:49.989Z"
)

res = response.json()
# print(res)
for r in res:
    print(r["id"])
    if r["corrector"] == "invisible":
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('America/New_York')
        utc = datetime.strptime(r["begin_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
        utc = utc.replace(tzinfo=from_zone)
        central = utc.astimezone(to_zone)

        print(f"invisible -> begin at:{central}")
    else:
        print(r["corrector"])

        for p in r["correcteds"]:
            print(p["login"])
    print("-----")
    # print(f"{r['corrector']['login']} will evaluate -> {r['correcteds'][0]['login']} -> id {r['id']}")
# Print response status and content
# print(response.status_code)
# print(response.text)
