import base64
import requests
import json

with open('config.json') as f:
    config = json.load(f)

archerBaseURL = config["archerConfig"]["baseURL"]

url = archerBaseURL + "/platformapi/core/security/login"

requestBody = {
    "InstanceName": config["archerConfig"]["instance"],
    "Username": config["archerConfig"]["username"],
    "UserDomain": "",
    "Password": config["archerConfig"]["password"]
}
requestHeaders = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=requestBody, headers=requestHeaders)

responseBody = json.loads(response.text)
sessionToken = responseBody["RequestedObject"]["SessionToken"]
print(sessionToken)

recordUrl = archerBaseURL + "/platformapi/core/content/contentid?id=348575"

headers = {
    "Authorization": "Archer session-id=\"" + sessionToken + "\"",
    "Content-Type": "application/json"
}

response = requests.get(recordUrl, headers=headers)

contentBody = json.loads(response.text)
levelId = contentBody["RequestedObject"]["LevelId"]

url = archerBaseURL + "/platformapi/core/system/fielddefinition/level/" + str(levelId)

response = requests.get(url, headers=headers)
#print(response.text)


snowBaseURl = config["servicenowConfig"]["baseURL"]
url = snowBaseURl + "/api/now/table/sys_user?sysparm_limit=10"

basicAuthToken = config["servicenowConfig"]["username"] + ":" + config["servicenowConfig"]["password"]
authString = base64.b64encode(basicAuthToken.encode()).decode('utf-8')
print(authString)

headers = {
    "Accept": "application/json",
    "Authorization": "Basic " + authString
}

response = requests.get(url, headers=headers)

print(response.text)