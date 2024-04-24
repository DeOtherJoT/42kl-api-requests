from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
from datetime import datetime as dt, timedelta
import os
import json
import colorama
from colorama import Fore

colorama.init(autoreset=True)

load_dotenv()

# Yay API token stuff
UID = os.getenv("42-UID")
SECRET = os.getenv("42-SECRET")

if UID == None or SECRET == None:
	raise (Exception("Env variables are not defined!"))

SITE = "https://api.intra.42.fr"
SCOPE = "public"

client = BackendApplicationClient(client_id=UID)
oauth = OAuth2Session(client=client)

token = oauth.fetch_token(
	token_url=f"{SITE}/oauth/token", client_id=UID, client_secret=SECRET, scope=SCOPE
)

# Get the ID of the user using a simple GET
intra_id = input(f"{Fore.YELLOW}Type in the intra id of the user: ").lower()

get_student_id = oauth.get(f"{SITE}/v2/users/{intra_id}")
if (get_student_id.status_code == 200):
	print(f"{Fore.GREEN}User {intra_id} found!")
else:
	print(f"{Fore.RED}User {intra_id} is not found!")
	raise (Exception("User with intra ID is not found."))

student_data = json.loads(get_student_id.text)
student_id = student_data["id"]

# Get the ID of the exam, manual for now
exam_id = 17852

# Build payload
payload = {
	"exams_user": {
		"user_id": student_id
    }
}

response = oauth.post(f"{SITE}/v2/exams/{exam_id}/exams_users", json=payload)

if (response.status_code == 201):
	color = Fore.GREEN
else:
	color = Fore.RED

print(f"{color}{response.status_code} {response.text}")