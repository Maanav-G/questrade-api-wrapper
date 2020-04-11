import requests
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('config.cfg')

api_server = parser.get('creds', 'api_server')
rest_opr = "accounts"
uri = api_server + "/v1/" + rest_opr

token_type = parser.get('creds', 'token_type')
access_token = parser.get('creds', 'access_token')
autho = token_type + ' ' + access_token

headers = {'Authorization': autho }

r = requests.get(uri, headers=headers)
response = r.json()

print(response)


