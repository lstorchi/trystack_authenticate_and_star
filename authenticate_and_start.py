import requests
import json
import os

from sets import Set

userid = str( os.getenv( "OS_USERNAME" ))
password = str( os.getenv( "OS_PASSWORD"))

# get tokenid
url = 'http://x86.trystack.org:5000/v2.0/tokens'
headers = {'content-type': 'application/json'}
payload = {'auth':{'passwordCredentials':{'username': userid, \
    'password':password}, 'tenantId':''}}    
r = requests.post(url, data=json.dumps(payload), headers=headers)
#print r.headers.get('content-type')
#print json.dumps(r.json(), sort_keys=True, indent=4, separators=(',', ': '))
json_data = r.json()
r.close()
tokens = json.loads(json.dumps(json_data))
#print tokens
tokenid = tokens['access']['token']['id']

# get tenant id 
url = 'http://x86.trystack.org:5000/v2.0/tenants'
headers = {'X-Auth-Token':str(tokenid)}
#print headers
r = requests.get(url, headers=headers)
#print r.headers.get('content-type')
#print json.dumps(r.json(), sort_keys=True, indent=4, separators=(',', ': '))
json_data = r.json()
r.close()
tokens = json.loads(json.dumps(json_data))
tenatid = tokens['tenants'][0]['id']

#get real token
url = 'http://x86.trystack.org:5000/v2.0/tokens'
headers = {'content-type': 'application/json'}
payload = {'auth':{'passwordCredentials':{'username': userid, \
    'password':password}, 'tenantId':str(tenatid)}}
r = requests.post(url, data=json.dumps(payload), headers=headers)
#print json.dumps(r.json(), sort_keys=True, indent=4, separators=(',', ': '))
json_data = r.json()
r.close
tokens = json.loads(json.dumps(json_data))
tokenid = tokens['access']['token']['id']

#get ceilometer publicurl
adminurl = ""
for item in tokens['access']['serviceCatalog']:
  if (item['type'] == 'metering'):
    #print item['name']
    #print item['endpoints'][0]
    publicURL = item['endpoints'][0]['publicURL']

# get meters     
url = publicURL + "/v2/meters/"
headers = {'X-Auth-Token':str(tokenid)}
r = requests.get(url, headers=headers)
#print json.dumps(r.json(), sort_keys=True, indent=4, separators=(',', ': '))
json_data = r.json()
r.close()
tokens = json.loads(json.dumps(json_data))
projects = Set()
users = Set()
for item in tokens:
  projects.add(item['project_id'])
  users.add(item['user_id'])
  #print item['resource_id']

print "Num. of projects: ", len(projects)
for proj in projects:
  print "  ", proj

userid = ""
print "Num. of users: ", len(users)
for user in users:
  print "  ", user
  if user != "None":
    userid = user

print "Ask for user: ", userid
