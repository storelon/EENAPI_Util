import requests

import get_account as ga
import set_account as sa

def menu_account(cookie):
    while True:
        print('1 to display sub account list, 2 to change account, 3 to download account list,')
        print('4 to return to master account, 0 to return to menu.')
        mode = raw_input('>>> ')
        if mode == '1':
            ga.accountlist(cookie)
        elif mode == '2':
            sa.change_account(cookie)
        elif mode == '3':
            ga.dl_accountlist(cookie)
        elif mode == '4':
            sa.reset_account(cookie)
        elif mode == '0':
            print('Return to menu.')
            break
