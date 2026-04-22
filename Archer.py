import requests
import json
import xmltodict
import math

class archer:
    def __init__(self):
        with open('config.json') as f:
            config = json.load(f)
        self.baseURL = config["archerConfig"]["baseURL"]
        self.username = config["archerConfig"]["username"]
        self.password = config["archerConfig"]["password"]
        self.instance = config["archerConfig"]["instance"]
        self.sessionToken = ""
        self.csrf_token = ""
        self.headers = {
            "Content-Type": "application/json"
        }
        self.soapHeader = {"Content-Type": "application/x-www-form-urlencoded"}
        self.login()
        self.headers = {
            "Authorization": "Archer session-id=\"" + self.sessionToken + "\"",
            "Content-Type": "application/json"
        }


    def login(self):
        url = self.baseURL + "/platformapi/core/security/login"
        requestBody = {
            "InstanceName": self.instance,
            "Username": self.username,
            "UserDomain": "",
            "Password": self.password
        }
        response = requests.post(url, json=requestBody, headers=self.headers)
        responseBody = json.loads(response.text)
        self.sessionToken = responseBody["RequestedObject"]["SessionToken"]
        return self.sessionToken
    
    def csrfToken(self):
        url = self.baseURL + "/api/V2/internal/LookUp?node=root"
        headers = {"Cookie": "__ArcherSessionCookie__=" + self.sessionToken}
        response = requests.get(url, headers=headers)
        headers_dict = dict(response.headers)
        if 'csrf-token' in headers_dict:
            self.csrf_token = headers_dict['csrf-token']
            self.headers['x-csrf-token'] = self.csrf_token
        
        
    def updateContent(self, applicationName, record):
        url = self.baseURL + "/contentapi/" + applicationName
        response = requests.post(url, json=record, headers=self.headers)
        print(response)
        responseBody = response.json()
        print(responseBody)
        return responseBody["RequestedObject"]["ContentId"]

    def updateRecord(self, recordDetails):
            response = requests.put(self.baseURL+"/platformapi/core/content", headers=self.headers, json=recordDetails)
            data = json.loads(response.content)
            archerReqSuccess = False
            if response.status_code == 200:
                archerReqSuccess = data.get("IsSuccessful", False)
            else:
                print("Request Failed:", response.status_code, data)
            if archerReqSuccess:
                recordId = data["RequestedObject"]["Id"]
                print("Record updated with Id - ",recordId)
                return recordId

    def createRecord(self, recordDetails):
            response = requests.post(self.baseURL+"/platformapi/core/content", headers=self.headers, json=recordDetails)
            data = json.loads(response.content)
            archerReqSuccess = False
            if response.status_code == 200:
                archerReqSuccess = data.get("IsSuccessful", False)
            else:
                print("Request Failed:", response.status_code, data)
            if archerReqSuccess:
                recordId = data["RequestedObject"]["Id"]
                print("Record created with Id - ",recordId)
                return recordId

    def getRecords(self, reportIdOrGuid, pageNumber):
        url = self.baseURL + "/ws/search.asmx/SearchRecordsByReport"
        requestBody = {
            "sessionToken": self.sessionToken,
            "reportIdOrGuid": reportIdOrGuid,
            "pageNumber": pageNumber
        }
        response = requests.post(url, data=requestBody, headers=self.soapHeader)
        outer = xmltodict.parse(response.text)
        inner_xml_escaped = outer['string']['#text']
        inner_dict = xmltodict.parse(inner_xml_escaped)
        json_output = json.dumps(inner_dict, indent=2)
        if str(pageNumber) == "1":
            records = json.loads(json_output)
            totalRecords = int(records["Records"]["@count"])
            if(totalRecords > 0):
                recordsArray = records["Records"]["Record"]
                if not isinstance(recordsArray, list):
                    recordsArray = [recordsArray]
                    records["Records"]["Record"] = recordsArray
                reportSize = len(recordsArray)
                if reportSize > 0:
                    count = totalRecords / reportSize
                    counter = math.ceil(count)
                    for i in range(2, counter + 1):
                        record2_str = self.getRecords(reportIdOrGuid, i)
                        record2 = json.loads(record2_str)
                        record2_array = record2["Records"].get("Record", [])
                        if not isinstance(record2_array, list):
                            record2_array = [record2_array]
                        recordsArray.extend(record2_array)
                return json.dumps(records, indent=2)
        return json_output

    def getFieldsByLevelId(self, levelId):
        url = self.baseURL + "/platformapi/core/system/fielddefinition/level/" + str(levelId)
        response = requests.get(url, headers=self.headers)
        return response.json()