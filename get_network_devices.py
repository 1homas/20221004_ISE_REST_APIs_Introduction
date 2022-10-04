#!/usr/bin/env python3

import requests

url = "https://ise.securitydemo.net:443/ers/config/networkdevice/"

payload={}
headers = {
  'Accept': 'application/json',
  'Authorization': 'Basic YWRtaW46SVNFaXNSZWFsbHlDMDBMIQ=='
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

