import json
from Archer import archer
from ServiceNow import servicenow
import os
import re
os.system('cls' if os.name == 'nt' else 'clear')

with open('config.json') as f:
    config = json.load(f)
    mapping = config["mapping"]


# Sync Archer Records in ServiceNow
archerAPI = archer()
snowAPI = servicenow()
"""records_text = archerAPI.getRecords(config["sourceApplicationReportId"], "1")
records = json.loads(records_text)
recordsArray = records["Records"]["Record"]

def strip_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

for record in recordsArray:
    #print(record)
    snow_request = {}
    fieldsData = record["Field"]
    archerRecordId = record["@contentId"]
    for field in fieldsData:
        fieldId = field["@id"]
        fieldType = field["@type"]
        for map in mapping:
            mappedId = map["archerFieldId"]
            if(fieldId == mappedId):
                if(fieldType == "4"):
                    listValueMapping = map["listMapping"]
                    filedListValue = field["ListValues"]["ListValue"]["#text"]
                    snow_request[map["servicenowFieldId"]] = listValueMapping[filedListValue]
                else:
                    value = field.get("#text", "")
                    snow_request[map["servicenowFieldId"]] = strip_html_tags(value)
    if(snow_request["sys_id"] == ""):
        print("Creating record in ServiceNow")
        snowSysId = snowAPI.createRecord(config["targetApplication"], snow_request)
        archerRequest = {}
        archerRequest["Content"] = {}
        archerRequest["Content"]["Id"] = archerRecordId
        archerRequest["Content"]["LevelId"] = config["sourceApplicationLevelId"]
        archerRequest["Content"]["FieldContents"] = {}
        archerRequest["Content"]["FieldContents"]["28786"] = {}
        archerRequest["Content"]["FieldContents"]["28786"]["Type"] = 1
        archerRequest["Content"]["FieldContents"]["28786"]["Value"] = snowSysId
        archerRequest["Content"]["FieldContents"]["28786"]["FieldId"] = 28786
        print(archerRequest)
        archerUpdatedRecord = archerAPI.updateRecord(archerRequest)
    else:
        print("Updating record in ServiceNow")
        snowAPI.updateRecord(config["targetApplication"], snow_request["sys_id"], snow_request)
"""
        
# Sync ServiceNow Records in Archer
query = "sys_updated_on>=javascript:gs.beginningOfYesterday()"
fields = "u_archer_irm_record_id,description,short_description,state,sys_id"
snowRecords = snowAPI.getRecords(config["targetApplication"], query, fields)
snowData = snowRecords["result"]
for snowRecord in snowData:
    archerRecordId = snowRecord["u_archer_irm_record_id"]
    archerRequest = {}
    archerRequest["Content"] = {}
    archerRequest["Content"]["LevelId"] = config["sourceApplicationLevelId"]
    archerRequest["Content"]["FieldContents"] = {}
    archerRequest["Content"]["FieldContents"]["28786"] = {}
    archerRequest["Content"]["FieldContents"]["28786"]["Type"] = 1
    archerRequest["Content"]["FieldContents"]["28786"]["Value"] = snowRecord["sys_id"]
    archerRequest["Content"]["FieldContents"]["28786"]["FieldId"] = 28786
    archerRequest["Content"]["FieldContents"]["2670"] = {}
    archerRequest["Content"]["FieldContents"]["2670"]["Type"] = 1
    name = snowRecord["short_description"]
    if(name == ""):
        name = "Not Available"
    archerRequest["Content"]["FieldContents"]["2670"]["Value"] = name
    archerRequest["Content"]["FieldContents"]["2670"]["FieldId"] = 2670
    archerRequest["Content"]["FieldContents"]["2265"] = {}
    archerRequest["Content"]["FieldContents"]["2265"]["Type"] = 1
    description = snowRecord["description"]
    if(description == ""):
        description = "Not Available"
    archerRequest["Content"]["FieldContents"]["2265"]["Value"] = description
    archerRequest["Content"]["FieldContents"]["2265"]["FieldId"] = 2265
    print(archerRequest)
    if(archerRecordId != ""):
        print("Updating record in Archer")
        archerRequest["Content"]["Id"] = archerRecordId
        archerAPI.updateRecord(archerRequest)
    else:
        print("Creating record in Archer")
        archerRecordId = archerAPI.createRecord(archerRequest)
        snowRequest = {
            "u_archer_irm_record_id": archerRecordId,
            "short_description": name
            }
        snowAPI.updateRecord(config["targetApplication"], snowRecord["sys_id"], snowRequest)

            
