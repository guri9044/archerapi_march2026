import requests

url = "https://dev341823.service-now.com/api/now/table/sys_user?sysparm_limit=10"

headers = {
    "Accept": "application/json",
    "Authorization": "Basic YWRtaW46UEsxRXdWOSF5eF5x" 
}

response = requests.get(url, headers=headers)

print(response.text)