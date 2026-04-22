import requests

url = "https://archer-irm.com/Archer/contentapi/Findings(348575)"

headers = {
    "Cookie": "__ArcherSessionCookie__=270EFE1DBCBDD945593B009EBF0D3128"
}

response = requests.get(url, headers=headers)
responseCode = response.status_code
if(responseCode == 200):
    print(response.json())
else:
    print("Failure")