import requests 
from ConfigParser import SafeConfigParser
import refresh

parser = SafeConfigParser()
parser.read('info/config.cfg')

id_ = parser.get('creds', 'id')

# def refresh_():
#     refresh.activate_refresh_key()

def get_headers():
    parser = SafeConfigParser()
    parser.read('info/config.cfg')
    token_type = parser.get('creds', 'token_type')
    access_token = parser.get('creds', 'access_token')
    autho = token_type + ' ' + access_token
    headers = {'Authorization': autho }
    return headers

def get_uri():
    parser = SafeConfigParser()
    parser.read('info/config.cfg')
    api_server = parser.get('creds', 'api_server')
    uri = api_server + "v1/"
    return uri

def req(uri, headers):
    r = requests.get(uri, headers=headers)
    response = r.json()
    return response 

def get_(rest_opr):
    uri = get_uri() + rest_opr
    headers = get_headers()
    return req(uri, headers)