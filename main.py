import os, sys

from een_auth import auth
from een_video import dl_videos as dv
from een_account import operate_account as oa
from een_device import menu_device as md
from een_localize import language


def apitool_main():
    authentica = auth.Auth() #Create a instance of authentication class.
    cookie = authentica.get_cookie() #Get a cookie.
    lang = language.Language('main') #Create a instance of language localization class.

    def printer(string): #printer method
        print(string.replace('\n',''))
    
    while True:
        [printer(lang.getStrings(x)) for x in range(5)]
        '''
        1 to device information menu
        2 to download videos
        3 to change to subaccount
        9 to exit with logout
        0 to exit without logout
        '''
        mode = raw_input('>>> ')
        if mode == '1': #Go to devicelist menu.
            md.menu_bridgeinfo(cookie)
        elif mode == '2': #Go to download video menu.
            dv.downloadvideos(cookie)
        elif mode == '3': #Go to subaccount menu.
            oa.menu_account(cookie)
        elif mode == '9': #exit with logout
            authentica.logout()
            print(lang.getStrings(5))
            #Exiting.
            break
        elif mode == '0': #exit without logout
            print(lang.getStrings(5))
            #Exiting.
            break

if __name__ == '__main__': #main method
    apitool_main()
