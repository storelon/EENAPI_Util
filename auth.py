import json
import requests, requests.utils, pickle
import pprint
import sys
import os
import certifi
from getpass import getpass

cookie_file = 'cookie'

#I don't know why but py2exed program wouldn't make cacert.pem
#os.environ['REQUESTS_CA_BUNDLE'] = "./certifi/cacert.pem"

def get_cookie():
    try:
        with open(cookie_file, 'r') as f:
            cookie = requests.utils.cookiejar_from_dict(pickle.load(f))
        response = requests.get('https://login.eagleeyenetworks.com/g/account/list', cookies=cookie)
        if response.status_code == 200:
            return(cookie)
        else:
            print('Invalid cookie or the cookie has expired.')
            raise IncorrectCookieError
    except requests.exceptions.ConnectionError:
        print('Check internet connection!!!')
        sys.exit()
    except:
        uid = userinput()
        tfa_bool = False
        response = requests.post('https://login.eagleeyenetworks.com/g/aaa/authenticate', {'username':uid[0],'password':uid[1]})

        print(response)
        try :
            token = response.json()['token']
        except :
            print('Login failure.')
            sys.exit()

        if 'two_factor_authentication_code' in response.json() :
            tfa_auth(response)
            tfa_bool = True

        if tfa_bool == False:
            response = requests.post('https://login.eagleeyenetworks.com/g/aaa/authorize', {'token':token})
        else:
            tfacode = raw_input('Enter the number you received for two factors authentication. >>> ')
            response = requests.post('https://login.eagleeyenetworks.com/g/aaa/authorize', {'token':token, 'two_factor_authentication_code': tfacode})
        print('Login success.')
        pprint.pprint('auth_key = ' + response.cookies['auth_key'])
        try:
            with open(cookie_file, 'w') as f:
                pickle.dump(requests.utils.dict_from_cookiejar(response.cookies), f)
        except:
            print('Cannot save cookie...')
        return(response.cookies)

def userinput():
    uid = ['mail','pass']
    uid[0] = raw_input('E-mail adress >>> ')
    uid[1] = getpass('Password >>> ')
    return uid

def logout(cookie):
    response = requests.post('https://login.eagleeyenetworks.com/g/aaa/logout', cookies=cookie)
    print(response)
    if response.status_code == 204:
        os.remove(cookie_file)
        print('Logout succeed.')
    else:
        print('Error. Logout failure.')

def tfa_auth(response):
    print('E-mail : ' + response.json()['two_factor_authentication_code']['email'])
    print('SMS : ' + response.json()['two_factor_authentication_code']['sms'])

    print('1 to send two factor authentication code to E-mail,')
    print('2 to send the code to SMS.')
    tfa_input = raw_input('>>> ')
    if tfa_input == '1':
        tfamode = 'email'
        print('I\'ll send a number to your E-mail address.')
    elif tfa_input == '2':
        tfamode = 'sms'
        print('I\'ll send a number to your SMS.')
    else:
        print('Quited two factor authentication.')
        print('Exited.')
        sys.exit()
    response2 = requests.post('https://login.eagleeyenetworks.com/g/aaa/two_factor_authenticate', {'token':response.json()['token'], 'two_factor_authentication_type':tfamode})
    print(response2)
    if response2.status_code == 200:
        print('Success to send the code.')
    else:
        print('Failed to send the code.')
        sys.exit()
