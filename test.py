from ConfigParser import SafeConfigParser
import requests

# parser = SafeConfigParser()
# parser.read('config.cfg')

# print (parser.get('creds', 'access_token'))

# parser.set('creds', 'token_type', 'Bull')


# print (parser.get('creds', 'token_type'))


def replace_values(access_token, api_server, refresh_token, token_type):
    parser = SafeConfigParser()
    parser.add_section('creds')
    parser.set('creds', 'access_token', access_token)
    parser.set('creds', 'api_server', api_server)
    parser.set('creds', 'refresh_token', refresh_token)
    parser.set('creds', 'token_type', token_type)
    with open('config.cfg', 'wb') as configfile:
        parser.write(configfile)


def refresh_key(refresh_token):
    refresh_server = "https://login.questrade.com/oauth2/token?grant_type=refresh_token&refresh_token="
    uri = refresh_server + refresh_token
    r = requests.get(uri)
    response = r.json()
    return response

test = refresh_key('9ATvv94QtXUbzwSF8U-ryLUdM38dbgGN0')

print(test)
print("ACCESS TOKEN - ")
print(test['access_token'])
print("SERVER - ")
print(test['api_server'])

