from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
from datetime import datetime as dt, timedelta
import os
import colorama
import time
from colorama import Fore

colorama.init(autoreset=True)

load_dotenv()

# Yay API token stuff
UID = os.getenv("42-UID")
SECRET = os.getenv("42-SECRET")
CAMPUS_ID = os.getenv("42-CAMPUS")

if None in [UID, SECRET, CAMPUS_ID]:
	raise (Exception("Env variables are not defined!"))

SITE = "https://api.intra.42.fr"
SCOPE = "public"

client = BackendApplicationClient(client_id=UID)
oauth = OAuth2Session(client=client)

token = oauth.fetch_token(
	token_url=f"{SITE}/oauth/token", client_id=UID, client_secret=SECRET, scope=SCOPE
)

# First create dt variables that represent the next Wednesday and next Saturday for the week.
# This script has to be run on either Sunday, Monday or Tuesday, otherwise the exams will be
# created for the following week.
dt_today = dt.now()
num_to_tues = 2 - int(dt_today.strftime("%w"))

dt_tues = dt_today + timedelta(days=num_to_tues)
if (num_to_tues <= 0):
	dt_tues += timedelta(days=7)
dt_thurs = dt_tues + timedelta(days=2)

tues_start = dt_tues.strftime("%Y-%m-%dT06:00:00.000Z")
tues_end = dt_tues.strftime("%Y-%m-%dT09:00:00.000Z")
thurs_start = dt_thurs.strftime("%Y-%m-%dT06:00:00.000Z")
thurs_end = dt_thurs.strftime("%Y-%m-%dT09:00:00.000Z")

# Get exam location - match it with the proper unit IP address.
print(f"{Fore.CYAN}\n[ EXAM LOCATION SELECTION ]\n")
choice_arr = [
	["Unit 180", "10.11.0.0/16"],
	["Unit 181", "10.12.0.0/16"],
	["Unit 182", "10.13.0.0/16"],
	["Unit 190", "10.14.0.0/16"],
	["Unit 191", "10.15.0.0/16"],
]
print(f"{Fore.CYAN}Your options are:\n[0] - Unit 180\n[1] - Unit 181\n[2] - Unit 182\n[3] - Unit 190\n[4] - Unit 191")
print(f"{Fore.CYAN}Please type in the index of the intended Units seperated by just commas.\nFor example, '1' stands for just Unit 181, '0,2' stands for Units 180 and 182.")
while (True):
	ip_range = []
	exam_location = []
	raw_input = input(f"{Fore.YELLOW}\nType in the index of the Exam Unit(s) (Default is 1): ")
	if (raw_input == ""):
		exam_location = choice_arr[1][0]
		ip_range = choice_arr[1][1]
		break
	try:
		input_vals = [int(i) for i in raw_input.split(',')]
		for item in input_vals:
			exam_location.append(choice_arr[item][0])
			ip_range.append(choice_arr[item][1])
		if len(exam_location) == 0:
			raise(Exception("You did not enter a valid exam location."))
		if len(exam_location) == 1:
			sep = ""
		else:
			sep = ", "
		exam_location = sep.join(exam_location)
		ip_range = sep.join(ip_range)
		break
	except Exception as err:
		print(f"{Fore.RED}[ ERROR ] - {err}\nTry again")
		continue

print(f"{Fore.CYAN}\nCurrent location is {exam_location}")
loc_var = input(f"{Fore.YELLOW}Type in new location or leave blank to keep default: ")
if (loc_var != ""):
	exam_location = loc_var

payloads = [
	{
		"exam": {
			"name": "Cadet Ranking Exam",
			"begin_at": tues_start,
			"end_at": tues_end,
			"location": exam_location,
			"ip_range": ip_range,
			"campus_id": f"{CAMPUS_ID}",
			"activate_waitlist": "false",
			"project_ids": [1320, 1321, 1322, 1323, 1324]
		}
	},
	{
		"exam": {
			"name": "Cadet Ranking Exam",
			"begin_at": thurs_start,
			"end_at": thurs_end,
			"location": exam_location,
			"ip_range": ip_range,
			"campus_id": f"{CAMPUS_ID}",
			"activate_waitlist": "false",
			"project_ids": [1320, 1321, 1322, 1323, 1324]
		}
	}
]

for payload in payloads:
	response = oauth.post(f"{SITE}/v2/exams", json=payload)

	if (response.status_code == 201):
		color = Fore.GREEN
	else:
		color = Fore.RED
	print(f"{color} {response.text}")

	time.sleep(0.5)