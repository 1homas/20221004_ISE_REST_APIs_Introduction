#!/usr/bin/env python

import requests
import json
requests.packages.urllib3.disable_warnings()

url = "https://ise.securitydemo.net:9060/ers/config/networkdevice"

payload={}
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Basic YWRtaW46SVNFaXNSZWFsbHlDMDBMIQ==',
  # 'Cookie': 'APPSESSIONID=32B75420553E6DD026D19CE4AB36EB04; JSESSIONIDSSO=2760D5BA41906E8283FC2D7687917A73'
}

resources = []
# loop over URLs
while (url) :
    # add resources to list
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resources += response.json()["SearchResult"]["resources"]
    try :
        url = response.json()["SearchResult"]["nextPage"]["href"]
    except Exception as e :
        url = None

# print resource names
for resource in resources :
    print(f'{resource["id"]} {resource["name"]}')

    # print networkdevice details
    url = "https://ise.securitydemo.net:9060/ers/config/networkdevice/"+resource["id"]
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    print(response.json())

    # PUT new RADIUS shared secret
    networkdevice = response.json()
    print(networkdevice)
    print('----')
    networkdevice["NetworkDevice"]["authenticationSettings"]['enableMultiSecret'] = True
    networkdevice["NetworkDevice"]["authenticationSettings"]['secondRadiusSharedSecret'] = "MySecondSharedSecret"
    payload = json.dumps(networkdevice)
    print('-----')
    response = requests.request("PUT", url, headers=headers, data=payload, verify=False)
    print(response.status_code)
