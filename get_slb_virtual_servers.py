import requests, json, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url_eu1 = 'https://10.17.232.38/services/rest/v2'
url_bo1 = 'https://10.50.240.25/services/rest/v2'
url_jp1 = 'https://10.60.232.39/services/rest/v2'

# updated credentials variable with python dictionary instead of json object
pw_bo1 = ('Enter password for BO1 load balancer : ')
pw_eu1 = ('Enter password for EU1 load balancer : ')
pw_jp1 = ('Enter password for JP1 load balancer : ')

credentials_eu1 = {
   "credentials":{
      "username":"admin",
      "password": pw_eu1
   }
}

credentials_bo1 = {
   "credentials":{
      "username":"admin",
      "password": pw_bo1
   }
}

credentials_jp1 = {
   "credentials":{
      "username":"admin",
      "password": pw_jp1
   }
}


json_header = {
    'Content-Type': 'application/json'
    }

req_bo1 = requests.post(
    url_bo1, json=credentials_bo1, headers=json_header, verify=False
)

req_eu1 = requests.post(
    url_eu1, json=credentials_eu1, headers=json_header, verify=False
)

req_jp1 = requests.post(
    url_jp1, json=credentials_jp1, headers=json_header, verify=False
)


print("\n")
print(f"The HTTP return status code is: {req_bo1.status_code}")
print("\n")
print(req_bo1.request.headers)
print("\n")
print(f"The method used is {req_bo1.request.method}")
print("\n")
print(req_bo1.text)

print("\n")
print(f"The HTTP return status code is: {req_eu1.status_code}")
print("\n")
print(req_eu1.request.headers)
print("\n")
print(f"The method used is {req_eu1.request.method}")
print("\n")
print(req_eu1.text)

print("\n")
print(f"The HTTP return status code is: {req_jp1.status_code}")
print("\n")
print(req_jp1.request.headers)
print("\n")
print(f"The method used is {req_jp1.request.method}")
print("\n")
print(req_jp1.text)
