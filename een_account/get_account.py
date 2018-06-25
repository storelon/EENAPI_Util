import json
import requests
import os, sys

sys.path.append(os.getcwd())

from een_filer import operate_dir as od
from een_filer import export as xd
from een_localize import language

gcookie = '' #recycle cookie

def get_accountlist():
    '''
    Get subaccount list method.
    :return json: response of subaccount list
    '''
    response = requests.get('https://login.eagleeyenetworks.com/g/account/list', cookies=gcookie)
    print(response)
    return(response)

def accountlist(cookie):
    '''
    Display subaccount list method.
    :param string cookie: Current session's cookie.
    '''
    lang = language.Language('een_account/get_account')
    global gcookie
    gcookie = cookie
    accounts = get_accountlist()
    if accounts.status_code == 200:
        def printer(string):
            print(string)
        [printer(i[1] + ' (ID: ' + i[0] + ' )') for i in accounts.json()]
    elif accounts.status_code == 403:
        print(lang.getStrings(0).replace('\n',''))

def dl_accountlist(cookie):
    '''
    Download and write sub account list method.
    :param string cookie: Current session's cookie.
    '''
    global gcookie
    gcookie = cookie
    accounts = get_accountlist()
    xd.fileout(accounts, 'subaccountlist')
    