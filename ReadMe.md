# ReadMe



## ISE REST Operations Quick Reference

The basic curl commands for REST operations with ISE

### Create (POST)
The `--data` option may be used with a local file beginning with `@` or use inline JSON:
```sh
curl --include --insecure --location \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --user $ISE_REST_USERNAME:$ISE_REST_PASSWORD \
  --request POST {URL} \
  --data @filename.json
  --data '
{ 
  ...JSON Data...
}'
```


### Read (GET)

```sh
curl --include --insecure --location \
  --header 'Accept: application/json' \
  --user $ISE_REST_USERNAME:$ISE_REST_PASSWORD \
  --request GET {URL}
```

### Update (PUT)

```sh
curl --include --insecure --location \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --user $ISE_REST_USERNAME:$ISE_REST_PASSWORD \
  --request PUT {URL}
```

### Update (PATCH)

Available in ISE 3.2+

```sh
curl --include --insecure --location \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --user $ISE_REST_USERNAME:$ISE_REST_PASSWORD \
  --request PATCH {URL}
```

### Delete (DELETE)

```sh
curl --include --insecure --location \
  --header 'Accept: application/json' \
  --user $ISE_REST_USERNAME:$ISE_REST_PASSWORD \
  --request DELETE {URL}
```

## ▼▼ Start Demo Here ▼▼

### Enable ISE APIs

1. **☰ > Administration > System > Settings >  API Settings**
1. Select **API Service Settings** tab
    1. ✅  ERS (Read/Write) 
    1. ✅  Open API (Read/Write) 
    1. **Save** 


### Download ERS OpenAPIs

Download ERS OpenAPI file to local computer for use with Postman later!

### Swagger UI

1. Reveiw the swagger ui
1. Create a Repository

```json
{
    "name": "FTP",
    "protocol": "FTP",
    "serverName": "198.18.133.36",
    "path": "/",
    "userName": "ise",
    "password": "C1sco12345"
}
```

1. Perform a backup with the repository

### Review Admin Groups

1. **☰ > Administration > System > Admin Access > Administrators > Admin Groups**
    - **ERS Admin** : Full access permission to External RESTful Services (ERS) APIs. Admins assigned to this admin group can perform CRUD (POST, PUT, DELETE, and GET) operations.
    - **ERS Operator** : Read-only access permission to the External RESTful Services (ERS) APIs.

### Create API Admin Users

1. **☰ > Administration > System > Admin Access > Administrators > Admin Users**
1. **+ Add** > **Create an Admin User**
    Name: **`ers-admin`**
    Password: **`ISEisC00L`**
    Admin Groups: **ERS Admin**
    **Submit**
1. **+ Add** > **Create an Admin User**
    Name: **`ers-operator`**
    Password: **`ISEisC00L`**
    Admin Groups: **`ERS Admin`**
    **Submit**

### Network Devices

1. Go to 𑁔 > Administration > Network Resources > Network Devices
2. **+Add Network Device**
    Name: `lab-mr46-1`
    IP Address: `10.80.60.150/32`
    RADIUS Authentication Settings:
      Shared Secret : `ISEisC00L`
    **Save**

## curl Basics

  > curl is a tool for transfering data from or to a server. It supports these protocols: DICT, FILE, FTP, FTPS, GOPHER, GOPHERS, HTTP, HTTPS, IMAP, IMAPS, LDAP, LDAPS, MQTT, POP3, POP3S, RTMP, RTMPS, RTSP, SCP, SFTP, SMB, SMBS, SMTP, SMTPS, TELNET or TFTP. The command is designed to work without user interaction.

`curl` has many options!
- there is a short option format `-` and a long `--` option format:
```sh
curl --help
curl --help all
```

These are the most popular options that I use:
- `--head` : retrieve headers only
- `--include` : include the response headers in the output
- `--insecure` : disable certificate validation
- `--location` : follow redirects
- `--silent` : disable progress meter/bar
- `--output <file>` : Write output to `<file>` instead of stdout
- `--styled-output` : Enables the automatic use of bold font styles when writing HTTP headers
- `--verbose` : Makes curl verbose during the operation

Basic HTTP GET request:

```sh
curl http://ise.securitydemo.net
```

This returns  `301 Moved Permanently` 8-(

Use the  `--include` the response headers to make more sense of this:
Include the HTTP response headers in the output

```sh
curl --include  http://ise.securitydemo.net 
```

Update the redirect `Location` again and again and again!

```sh
curl --include  https://ise.securitydemo.net 
curl --include  https://ise.securitydemo.net:443/admin/
curl --include  https://ise.securitydemo.net:443/admin/login.jsp
```

And that is why I like to always use the `--location` option to automatically follow redirects!

```sh
curl --include --location  http://ise.securitydemo.net 
```

Allow insecure connections with demo or lab instances that do not have a signed certificate:

```sh
curl --include --location http://ise.trust0.net 
curl --include --insecure --location http://ise.trust0.net 
```




## ISE REST APIs

Now it is time to try an actual ISE API!
See all of the ISE API endpoints/resources @ https://cs.co/ise-api

Also note the resources for 
Managing APIs via APIs:
- [OpenAPI](https://developer.cisco.com/docs/identity-services-engine/v1/#!open-api)
- [ERS API](https://developer.cisco.com/docs/identity-services-engine/v1/#!ers-api)
Refer to [Versioning](https://developer.cisco.com/docs/identity-services-engine/v1/#!versioning) for When a specific API endpoint was first supported by ISE. You may need to upgrade to perform some of the things you see here today.

```sh
curl --include --location --insecure https://ise.securitydemo.net/ers/config/networkdevice
```

results in a 401 Unauthorized because we are not authorized API users.


### HTTP Basic Authentication

```sh
curl --include --location --insecure --user admin:ISEisC00L  https://ise.securitydemo.net/ers/config/networkdevice
```

Response:

```
HTTP/1.1 415 (Unsupported Media Type)
...
<?xml version="1.0" encoding="utf-8" standalone="yes"?><ns3:ersResponse operation="GET-getAll-networkdevice" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:ns3="ers.ise.cisco.com"><link rel="related" href="https://ise.securitydemo.net/ers/config/networkdevice" type="application/xml"/><messages><message type="ERROR" code="Resource media type exception"><title>Illegal Request Header:  one or more of 'accept' / 'content-type' / 'ers-media-type' headers is not supported.</title></message></messages></ns3:ersResponse>
```

### Accept XML Outut

Request XML output with the `Accept:` header:

```sh
curl --insecure --silent \
  --user admin:ISEisC00L \
  --header 'Accept: application/xml' \
  https://ise.securitydemo.net/ers/config/networkdevice \
```

XML in a long, concatenated string is not easy to read. You may use the Unix pipe (`|`) to redirect it to the xmllint program for pretty printing. A linter is a static code analysis tool for syntax checking.

> ⚠ You must remove `--include` or the linting will fail!

> 💡 Use `--silent` to remove the progress table 

> 💡 The final `-` at the end of the command tells xmllint to use `stdin` for the input

```sh
curl --insecure --silent \
  --user admin:ISEisC00L \
  --header 'Accept: application/xml' \
  https://ise.securitydemo.net/ers/config/networkdevice \
  | xmllint --pretty 1 -
```




### Accept JSON Output

Request JSON output instead of XML with the `Accept:` header:

```sh
curl --include --location --insecure --user admin:ISEisC00L --header 'Accept: application/json' https://ise.securitydemo.net/ers/config/networkdevice
```

YAY! Finally we got a JSON result from ISE!

### Port 9060 for ERS

For ISE versions before ISE 3.1, you will need to specify port 9060 when invoking the ERS APIs:

```sh
curl --include --location --insecure --user admin:ISEisC00L --header 'Accept: application/json' https://ise.securitydemo.net:9060/ers/config/networkdevice
```

If you are expecting JSON data and you get HTML instead, you either have not enabled APIs or you need to specify the port.




### Line Continuation

Are these command lines looking long? It's time to break them up so they are easier to read.  In the Unix bash shell, the backslash character `\` may be used to remove any special meaning for the next character read and ***for line continuation*** [bash manual](http://www.gnu.org/software/bash/manual/bashref.html). For line continuation, the backslash must be the last character on the line.

```sh
curl --include --insecure --location \
  --user admin:ISEisC00L \
  --header 'Accept: application/json' \
  https://ise.securitydemo.net/ers/config/networkdevice
```

You may also make JSON data pretty by piping the data through `jq`, a command line utility for performing JSON queries :
> ⚠ You must remove `--include` or the linting will fail!

```sh
curl --insecure --location --silent \
  --user admin:ISEisC00L \
  --header 'Accept: application/json' \
  https://ise.securitydemo.net/ers/config/networkdevice \
  | jq
```

`jq` is very powerful in extracting JSON data. If you only wanted the network device names, you could do:

```sh
curl --insecure --location --silent \
  --user admin:ISEisC00L \
  --header 'Accept: application/json' \
  https://ise.securitydemo.net/ers/config/networkdevice \
  | jq '.SearchResult.resources[].name'
```

It's not very interesting with only 1 network device but if you query against `endpointgroup` or `sgt` then you can begin to see the power.




### Environment Variables

**Environmental variables** are variables that are defined for the current shell and are inherited by any child shells or processes. Environmental variables are used to pass information into processes that are spawned from the shell. Use environment variables to [securely load and use your credentials](https://12factor.net/config) without showing anyone looking over your shoulder or in your terminal history. 
You may view all current environment variables with the `env` command and individual variables with `printenv`.
```sh
env
env | grep ISE
printenv ISE_REST_PASSWORD
```
> 💡 Environment variables traditionally are named in UPPERCASE while shell variables are lowercase

Define environment variables using the `export` command:

```sh

export ISE_REST_USERNAME=admin
export ISE_REST_PASSWORD=ISEisC00L
export ISE_HOSTNAME=ise.securitydemo.net
env | grep ISE
```

Use environment variables by referencing them with a `$`. You may show them individually using the `echo` command :

```sh
echo $ISE_REST_USERNAME $ISE_REST_PASSWORD $ISE_HOSTNAME
```

Now try a previous `curl` command using environment variables:

```sh
curl --insecure --location --silent \
  --user $ISE_REST_USERNAME:$ISE_REST_PASSWORD \
  --header 'Accept: application/json' \
  https://$ISE_HOSTNAME/ers/config/networkdevice
```

Save your environment variables in a text file in `~/.secrets/` directory for fast and easy loading later using the  `source` command:

```sh
ls -1 ~/.secrets
cat ~/.secrets/ise_azure.sh
cat ~/.secrets/ise_dcloud.sh
source ~/.secrets/ise_dcloud.sh
env | grep ISE
```




### GET ERS Details

We previously got information from the ISE ERS API for a network device :
```sh
curl --insecure --location --silent \
  --user $ISE_REST_USERNAME:$ISE_REST_PASSWORD \
  --header 'Accept: application/json' \
  https://$ISE_HOSTNAME/ers/config/networkdevice
```

but this only contains 4 attributes:

- `id`
- `name`
- `description`
- `link`

To get all of the configuration for a specific network device, you must use the `name` or `id` attributes which is what the link attribute was showing you:
```sh
curl --insecure --location --silent \
  --user $ISE_REST_USERNAME:$ISE_REST_PASSWORD \
  --header 'Accept: application/json' \
  https://$ISE_HOSTNAME/ers/config/networkdevice/{id}
```




### Result Size & Pages
GET profilerprofile (>600)

```sh
curl --insecure --silent \
  --user $ISE_REST_USERNAME:$ISE_REST_PASSWORD \
  --header 'Accept: application/json' \
  https://ise.securitydemo.net/ers/config/profilerprofile \
  | jq
```

GET the end of the profilerprofile list
```sh
curl --include --insecure --silent \
  --user $ISE_REST_USERNAME:$ISE_REST_PASSWORD \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  "https://ise.securitydemo.net/ers/config/profilerprofile?size=100\&page=7" \
  | jq
```


### Filtering

> 🐞 Filter does not return all of the matching resources! The matching result count is 4 but it only shows 1!

```sh
curl --include --insecure --silent \
  --user $ISE_REST_USERNAME:$ISE_REST_PASSWORD \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  https://ise.securitydemo.net/ers/config/profilerprofile?filter=name.STARTSW.i
```

## RBAC

### ers-admin

### ers-operator

### POST

### Create a new endpoint with `POST`

Find endpointgroup

```sh
curl --include --insecure --silent \
  --user $ISE_REST_USERNAME:$ISE_REST_PASSWORD \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  https://ise.securitydemo.net:9060/ers/config/endpointgroup \
  | jq -c .SearchResult.resources[] \
  | grep Meraki -
```

Create a new endpoint
```sh
curl --include --insecure --silent \
  --user $ISE_REST_USERNAME:$ISE_REST_PASSWORD \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  https://ise.securitydemo.net:9060/ers/config/endpoint \
  --data '
{
  "ERSEndPoint" : {
    "name" : "New Endpoint",
    "description" : "My Endpoint",
    "mac" : "FE:ED:DA:DD:BE:EF",
    "staticGroupAssignment" : true,
    "groupId" : "1e2700a0-8c00-11e6-996c-525400b48521"
  }
}'

## Response Header :
## HTTP/1.1 201 
## Location: https://ise.securitydemo.net:9060/ers/config/endpoint/0bd811b0-892f-11eb-b0e1-b2ca5a4c3815
```


### Create a new endpoint with custom attributes in a file

```sh
curl --include --insecure --silent \
  --user $ISE_REST_USERNAME:$ISE_REST_PASSWORD \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  https://ise.securitydemo.net:9060/ers/config/endpoint \
  --data @AC17C80C17A2.json
```


### Use POST to create a user
```sh
curl --include --insecure --silent \
  --user $ISE_REST_USERNAME:$ISE_REST_PASSWORD \
  --header 'Content-Type:application/json' \
  --header 'Accept: application/json' \
  https://$ISE_HOSTNAME:9060/ers/config/internaluser \
  --data '
{
    "InternalUser" : {
        "name" : "thomas",
        "password" : "ISEisC00L",
        "changePassword" : false
    }
}'
```

Do it again to get a 500 Error because the resource already exists!


### Create a Guest user

⚠ Requires `guestapi` user!

```sh
curl --include --insecure --silent \
  --user $guestapi_username:$guestapi_password \
  --header 'Content-Type:application/json' \
  --header 'Accept: application/json' \
  https://$ISE_HOSTNAME:9060/ers/config/guestuser \
  --data '
{
    "GuestUser": {
        "guestType": "Daily (default)",
        "portalId" : "bd48c1a1-9477-4746-8e40-e43d20c9f429",
        "guestInfo": {
            "enabled": "true",
            "userName": "rigo",
            "password": "ISEisC00L"
        },
        "guestAccessInfo": {
            "validDays": 1,
            "fromDate": "03/27/2021 17:40",
            "toDate": "03/28/2021 17:40",
            "location": "San Jose"
        }
    }
}'
```



## PUT 

### PUT/Update an endpoint

Cisco IP Phone

```sh
curl --include --insecure --silent \
  --user $ISE_REST_USERNAME:$ISE_REST_PASSWORD \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --request PUT https://ise.securitydemo.net:9060/ers/config/endpoint \
  --data '
{
  "ERSEndPoint" : {
    "name" : "IP Phone",
    "description" : "Thomas IP Phone",
    "mac" : "FE:ED:DA:DD:BE:EF",
    "staticGroupAssignment" : true,
    "groupId" : "14f5cac0-8c00-11e6-996c-525400b48521"
  }
}'
```

Response:

```json
## Response Header
## HTTP/1.1 200 

{
  "UpdatedFieldsList" : {
    "updatedField" : [ {
      "field" : "groupId",
      "oldValue" : "1e2700a0-8c00-11e6-996c-525400b48521",
      "newValue" : "14f5cac0-8c00-11e6-996c-525400b48521"
    }, {
      "field" : "description",
      "oldValue" : "My Endpoint",
      "newValue" : "Thomas IP Phone"
    } ]
  }
}
```

Change network device name or password


## PATCH

### GET HotspotPortal

GET hotspotportal (only 1) and look at the detail

```sh
curl --insecure --silent \
  --user $ISE_REST_USERNAME:$ISE_REST_PASSWORD \
  --header 'Accept: application/json' \
  https://ise.securitydemo.net/ers/config/hotspotportal \
  | jq
```

### GET HotspotPortal Details

```sh
curl --include --insecure --location \
  --header 'Accept: application/json' \
  --user $ISE_REST_USERNAME:$ISE_REST_PASSWORD \
  --request GET https://$ISE_HOSTNAME/ers/config/hotspotportal/{id}

```

### PATCH HotspotPortal Enable & Set Access Code

```sh
curl --include --insecure --location \
  --header 'Content-Type:application/json' \
  --header 'Accept: application/json' \
  --user $ISE_REST_USERNAME:$ISE_REST_PASSWORD \
  --request PATCH https://$ISE_HOSTNAME/ers/config/hotspotportal/{id}} \
  --data '
{
  "HotspotPortal": {
    "settings": {
       "aupSettings": {
          "requireAccessCode": true,
          "accessCode": "ISEisC00L"
       }
    }
  }
}'

```

### PATCH Change HotspotPortal Access Code

```sh
curl --include --insecure --location \
--header 'Content-Type:application/json' \
--header 'Accept: application/json' \
--user $ISE_REST_USERNAME:$ISE_REST_PASSWORD \
--request PATCH https://$ISE_HOSTNAME/ers/config/hotspotportal/{id} \
--data '
{
  "HotspotPortal": {
    "settings": {
      "aupSettings": {
        "accessCode": "ISEisC00LerNow"
      }
    }
  }
}'
```




## DELETE 

### DELETE NetworkDevice

```
curl  --include  --insecure  --location \
--header 'Content-Type:application/json' \
--header 'Accept: application/json' \
--user $ISE_REST_USERNAME:$ISE_REST_PASSWORD \
--request DELETE https://$ISE_HOSTNAME/ers/config/networkdevice/{id}

```


### Delete an Endpoint

```sh
curl --include --insecure --silent \
  --user $ISE_REST_USERNAME:$ISE_REST_PASSWORD \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --request DELETE  https://ise.securitydemo.net:9060/ers/config/endpoint/{id}
```


## Other uses of cURL

### HTTPS Probe for Guest Portal(s)
ISE 2.7+ portal responds with `HTTP/1.1 200` instead of `HTTP/1.1 200 OK`!
curl --include https://ise.securitydemo.net:8443/portal/PortalSetup.action?portal={id}




## Postman

### GUI Overview
- New Workspace
- Workspace Name : give your workspace a name
- Collections : your requests for an API
- APIs : Collections & environments with schemas
- Environments : sets of variables for use in context with requests




## Python

Install specific Python version and activate virtual environment

```sh
pipenv install --python 3.7
pipenv shell
pipenv install requests
```

Set a RADIUS secondary shared secret on all network devices
```sh
./second_radius_shared_secret.py
```

