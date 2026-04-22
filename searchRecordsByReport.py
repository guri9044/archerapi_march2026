import requests
import xmltodict
import json

url = "https://archer-irm.com/Archer/ws/search.asmx/SearchRecordsByReport"

payload = {
    "sessionToken": "270EFE1DBCBDD945593B009EBF0D3128",
    "reportIdOrGuid": "10410",
    "pageNumber": "1"
}
headers = {"Content-Type": "application/x-www-form-urlencoded"}

response = requests.post(url, data=payload, headers=headers)

outer = xmltodict.parse(response.text)
inner_xml_escaped = outer['string']['#text']
inner_dict = xmltodict.parse(inner_xml_escaped)
json_output = json.dumps(inner_dict, indent=2)
print(json_output)

