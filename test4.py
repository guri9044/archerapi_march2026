import json
from Archer import archer
from ServiceNow import servicenow
import os
import re
os.system('cls' if os.name == 'nt' else 'clear')
import requests

url = "https://archer-irm.com/Archer/contentapi/Findings"

payload = {
    "Findings_Id": 428138,
    "ServiceNow_Sys_Id": "snowSysId"
}
headers = {
    "Cookie": "__ArcherSessionCookie__=A3CE946CB00FBE50A74E1C8237C57570;",
    "x-csrf-token": "izIyWkpCuYlT7v5vhT7S0e_c820GKO8gQprcuVxxbPLEOfN6GxDzf9KHMAxojIA0__XVdTmNYeudgFLY0BgbQaInm92R1ZfPkfHy7KP9xLo1",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.status_code)          
