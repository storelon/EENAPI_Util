import requests
import sys, os

import get_account as ga
import set_account as sa

sys.path.append(os.getcwd())

from een_localize import language

def menu_account(cookie):
    '''
    Display menu of account list function.
    :param json cookie: Current session's cookie.
    '''
    lang = language.Language('een_account/operate_account')

    def printer(string):
        print(string.replace('\n',''))
    
    while True:
        [printer(lang.getStrings(x)) for x in range(6)]
        mode = raw_input('>>> ')
        if mode == '1': #Display subaccount list.
            ga.accountlist(cookie)
        elif mode == '2': #Change account.
            sa.change_account(cookie)
        elif mode == '3': #Download and output subaccount list.
            ga.dl_accountlist(cookie)
        elif mode == '4': #Return to master account.
            sa.reset_account(cookie)
        elif mode == '5': #Display Auth Key.
            print('auth_key = ' + cookie['auth_key'])
        elif mode == '0': #Return to menu.
            print(lang.getStrings(6))
            break
