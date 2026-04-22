import requests
import json
import base64

class servicenow:
    def __init__(self):
        with open('config.json') as f:
            config = json.load(f)
        self.baseURL = config["servicenowConfig"]["baseURL"]
        self.username = config["servicenowConfig"]["username"]
        self.password = config["servicenowConfig"]["password"]
        basicAuthToken = config["servicenowConfig"]["username"] + ":" + config["servicenowConfig"]["password"]
        self.authString = base64.b64encode(basicAuthToken.encode()).decode('utf-8')
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Basic " + self.authString
        }
    
    def getRecords(self, tableName, query, fields):
        url = self.baseURL + "/api/now/table/" + tableName + "?sysparm_query=" + query + "&sysparm_fields=" + fields
        response = requests.get(url, headers=self.headers)
        return response.json()

    def getRecord(self, tableName, recordId):
        url = self.baseURL + "/api/now/table/" + tableName + "/" + recordId
        response = requests.get(url, headers=self.headers)
        return response.json()  
    
    def createRecord(self, tableName, record):
        url = self.baseURL + "/api/now/table/" + tableName
        response = requests.post(url, json=record, headers=self.headers)
        responseBody = response.json()
        sysId = responseBody["result"]["sys_id"]
        print(sysId)
        return sysId
    
    def updateRecord(self, tableName, recordId, record):
        url = self.baseURL + "/api/now/table/" + tableName + "/" + recordId
        response = requests.put(url, json=record, headers=self.headers)
        responseBody = response.json()
        sysId = responseBody["result"]["sys_id"]
        print(sysId)
        return sysId
    
    