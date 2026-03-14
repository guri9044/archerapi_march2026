import requests

url = "https://archer-irm.com/Archer/contentapi/Findings(348575)"

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-IN,en-GB;q=0.9,en;q=0.8,en-US;q=0.7",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0",
    "sec-ch-ua": "\"Not:A-Brand\";v=\"99\", \"Microsoft Edge\";v=\"145\", \"Chromium\";v=\"145\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "Cookie": "__ArcherSessionCookie__=35B3B1781C5AD958860BEB7AD8B08715; ArcherBaseUrl=/Archer; SuppressPrivateFieldPlaceholderWarning=false; AppBuilderAutoSave=false"
}

response = requests.get(url, headers=headers)
responseCode = response.status_code
if(responseCode == 200):
    print(response.json())
else:
    print("Failure")