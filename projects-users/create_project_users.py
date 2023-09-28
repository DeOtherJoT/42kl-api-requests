import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import os
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
users = [
    # "schuah",
    # "plau",
    # "wxuerui",
    # "yetay",
    # "wricky-t",
    # "maiman-m",
    # "melee",
    # "hwong",
    # "nnorazma",
    # "kecheong",
    # "cteoh",
    # "yalee",
    # "chenlee",
    # "azhia-lo",
    # "maliew",
    # "lewlee",
    # "Welim",
    # "hqixeo",
    # "Syarham",
    # "zah",
    # "JAKOH",
    # "hloke",
    # "bleow",
    # "tkok-kea",
    # "wbin-wan",
    # "shechong",
    # "chlai",
    # "fizad",
    # "abin-zub",
    # "kkuah",
    # "folim",
    # "steh",
    # "welow",
    # "lyip",
    # "eloh",
    # "jgraceso",
    # "rsoo",
    # "kiloh",
    # "tjun-yu",
    # "cwoon",
    # "afiali",
    # "lzi-xian",
    # "mmuhamad",
    # "Jiachang",
    # "itan",
    # "Yichan",
    # "suchua",
    # "Yyap",
    # "rchoy",
    # "lcherng-",
    # "gdaryl",
    # "yichong",
    # "jthor",
    # "hyun-zhe",
    # "edlim",
    # "jehiew",
    # "djin",
    # "Aheng",
    # "amaligno",
    # "jyalee",
    # "rteoh",
    # "ychng",
    # "salmoham",
    # "wyap",
    # "atok",
    # "jyim",
    # "jatan",
    # "awee",
    # "sgan",
    # "phiew",
]
payload = {
    "projects_user": {
        "project_id": "",
        "user_id": "",
        "skip_check_permission": "true",
    }
}

project_ids = ["2267", "2268", "2269", "2270", "2271", "2272"]

# Make a request for each user and each project
for user in users:
    payload["projects_user"]["user_id"] = oauth.get(f"{SITE}/v2/users/{user.lower()}").json()["id"]
    for project_id in project_ids:
        payload["projects_user"]["project_id"] = project_id
        response = oauth.post(f"{SITE}/v2/projects_users", json=payload)
        # Print response status and content
        print(response.status_code)
        print(response.text)
        time.sleep(0.5)
