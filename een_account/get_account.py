import json
import requests
import os, sys

sys.path.append(os.getcwd())

from een_filer import operate_dir as od
from een_filer import export
from een_localize import language

def get_accountlist(cookie):
    '''
    Get subaccount list method.
    :param string cookie: Current session's cookie.
    :return json: response of subaccount list
    '''
    response = requests.get('https://login.eagleeyenetworks.com/g/account/list', cookies=cookie)
    print(response)
    return(response)

def accountlist(cookie):
    '''
    Display subaccount list method.
    :param string cookie: Current session's cookie.
    '''
    lang = language.Language('een_account/get_account')
    accounts = get_accountlist(cookie)
    if accounts.status_code == 200:
        def printer(string):
            print(string)
        [printer(i[1] + ' (ID: ' + i[0] + ' )') for i in accounts.json()]
    elif accounts.status_code == 403:
        print(lang.getStrings(0).replace('\n',''))
        #You have no subaccount because you are not a master account.

def dl_accountlist(cookie):
    '''
    Sub account list download and write method.
    :param string cookie: Current session's cookie.
    '''
    accounts = get_accountlist(cookie)
    filer = export.Filer()
    filer.fileout(accounts, 'subaccountlist')

def subaccountlist(cookie):
    '''
    Make a current user's sub account list and return the sub account list.
    :param string cookie: Current session's cookie.
    :param list accounts: Subaccount's list --->[account name, account id]
    '''
    lang = language.Language('een_account/get_account')
    print(lang.getStrings(1).replace('\n',''))
    #Checking subaccounts.
    response = get_accountlist(cookie)
    if response.status_code == 200:
        print(lang.getStrings(2).replace('\n',''))
        #Subaccounts found.
        accounts = [[],[]]
        [accounts[0].append(i[0]) for i in response.json()]
        [accounts[1].append(i[1]) for i in response.json()]
    else:
        print (lang.getStrings(3).replace('\n',''))
        #No subaccounts was found.
        accounts = None
    return accounts
