import requests
import urllib3

## disable warning for certificate verification
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

base_url = "https://10.10.20.60"        # need to change
username = "admin"                      # need to change
password = "1vtG@lw@y"                  # need to change
ssl_verify = False
headers = { "Content-Type": "text/plain" }
template_list = []

## Get Login token
payload = '{ "userName": "' + username + '", "userPasswd": "' + password + '", "domain": "local" }'
response = requests.request(
    "POST", 
    base_url + "/login", 
    headers=headers, 
    data=payload, 
    verify=ssl_verify
)
headers["Cookie"] = "AuthCookie=" + response.json()["jwttoken"]

## Get NDFC Template list
response = requests.request(
    "GET",
    base_url + "/appcenter/cisco/ndfc/api/v1/configtemplate/rest/config/templates/",
    headers=headers,
    data="",
    verify=ssl_verify
)
for item in response.json():
    template_list.append({"name": item["name"], "filename": item["fileName"]})

## Download NDFC Templates
for item in template_list:
    print(item)
    response = requests.request(
        "GET",
        base_url
        + "/appcenter/cisco/ndfc/api/v1/configtemplate/rest/config/templates/"
        + item["name"],
        headers=headers,
        data="",
        verify=ssl_verify
    )
    content = response.json()["content"]
    with open(item["filename"], "w") as f:
        f.write(content)
