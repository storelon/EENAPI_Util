import requests
import sys, os

sys.path.append(os.getcwd())

from een_localize import language

def set_account(account, cookie):
    '''
    Set current master account as a specified subaccount.
    :param string acount: Sub account's ID
    :param string cookie: Current session's cookie.
    :return json response: Answer of setting account from EEN.
    '''
    response = requests.post('https://login.eagleeyenetworks.com/g/aaa/switch_account', {'account_id': account}, cookies=cookie)
    print(response)
    return(response)

def reset_account(cookie):
    '''
    Reset current master account.
    :param strings cookie: Current session's cookie.
    '''
    lang = language.Language('een_account/set_account')
    response = requests.post('https://login.eagleeyenetworks.com/g/aaa/switch_account', cookies=cookie)
    print(response)
    if response.status_code == 200:
        print(lang.getStrings(0).replace('\n',''))
        #Success returning to master account.        
    else:
        print(lang.getStrings(1).replace('\n',''))
        #Account change failed.

def change_account(cookie):
    '''
    Change account method. Ask subaccount's ID and
    set current master account as a specified subaccount
    with set_account method.
    :param strings cookie: Current session's cookie.
    '''
    lang = language.Language('een_account/set_account')

    print(lang.getStrings(2).replace('\n',''))
    #Type sub account ID
    print(lang.getStrings(3).replace('\n',''))
    #Or type "0" to return to menu
    
    account = raw_input('>>> ') #Ask subaccount ID
    if account == 0: #Returning to menu.
        print(lang.getStrings(4).replace('\n',''))
        #Return to menu.
    else: #Change account.
        response = set_account(account, cookie)
        if response.status_code == 200:
            print(lang.getStrings(5).replace('\n',''))
            #Account change success.
        else:
            print(lang.getStrings(1).replace('\n',''))
            #Account change failed.
