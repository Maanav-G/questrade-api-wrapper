from ConfigParser import SafeConfigParser
import requests
import call

def replace_values(access_token, api_server, refresh_token, token_type):
    parser = SafeConfigParser()
    parser.add_section('creds')
    parser.set('creds', 'access_token', access_token)
    parser.set('creds', 'api_server', api_server)
    parser.set('creds', 'refresh_token', refresh_token)
    parser.set('creds', 'token_type', token_type)
    parser.set('creds', 'id', call.id_)
    with open('./info/config.cfg', 'wb') as configfile:
        parser.write(configfile)

def activate_refresh_key():
    config = SafeConfigParser()
    config.read('./info/config.cfg')
    refresh_token = config.get('creds', 'refresh_token')
    refresh_server = "https://login.questrade.com/oauth2/token?grant_type=refresh_token&refresh_token="
    uri = refresh_server + refresh_token
    r = requests.get(uri)
    response = r.json()
    new_access_token = response['access_token']
    new_api_server = response['api_server']
    new_refresh_token = response['refresh_token']
    new_token_type = response['token_type']
    replace_values(new_access_token, new_api_server, new_refresh_token, new_token_type)
    print('refreshed')
