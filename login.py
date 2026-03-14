import requests
import json

url = "https://archer-irm.com/Archer/platformapi/core/security/login"

requestBody = {
    "InstanceName": "t202603",
    "Username": "api.user",
    "UserDomain": "",
    "Password": "Archer@123"
}
requestHeaders = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=requestBody, headers=requestHeaders)

responseBody = json.loads(response.text)
sessionToken = responseBody["RequestedObject"]["SessionToken"]
print(sessionToken)

recordUrl = "https://archer-irm.com/Archer/platformapi/core/content/contentid?id=348575"

headers = {
    "Authorization": "Archer session-id=\"" + sessionToken + "\"",
    "Content-Type": "application/json"
}

response = requests.get(recordUrl, headers=headers)

contentBody = json.loads(response.text)
levelId = contentBody["RequestedObject"]["LevelId"]

url = "https://archer-irm.com/Archer/platformapi/core/system/fielddefinition/level/" + str(levelId)

response = requests.get(url, headers=headers)
print(response.text)