import requests

url = "https://archer-irm.com/Archer/platformapi/core/system/user"

payload = {
    "User": {
        "UserName": "test1234",
        "FirstName": "John",
        "LastName": "Doe"
    },
    "Password": "NewUser2005!"
}
headers = {
    "Authorization": "Archer session-id=\"8F70794A378AE67E34FBDC268B05D912\"",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)