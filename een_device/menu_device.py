import json
import requests
import sys, os

sys.path.append(os.getcwd())

from een_filer import export as xd
from een_localize import language

cookie = ''

def devicelist(gcookie):
    '''
    Menu of device list.
    :param string gcookie: current session's cookie.
    '''
    lang = language.Language('een_device/get_devicelist')
    global cookie
    cookie = gcookie
    while True:



def menu_bridgeinfo(cookie):
    '''
    Display this package's menu.
    :param string cookie: Current session's cookie.
    '''
    lang = language.Language('een_device/get_bridge')
    global gcookie
    gcookie = cookie
    while True:
        print(lang.getStrings(5).replace('\n',''))
        #1 to show bridge list
        print(lang.getStrings(6).replace('\n',''))
        #2 to download bridge's information
        print('3 to display bridge metrics')
        print('4 to bridge metrics to export CSV')
        print(lang.getStrings(7).replace('\n',''))
        #0 to return to menu
        print(lang.getStrings(1).replace('\n',''))
        #1 to output raw JSON
        print(lang.getStrings(2).replace('\n',''))
        #2 to export CSV
        print(lang.getStrings(3).replace('\n',''))
        #0 to return to menu
        mode = raw_input('>>> ')
        if mode == '1': #Show bridge list
            show_bridges()
        elif mode == '2': #Download bridge's information
            dl_bridgeinfo()
        elif mode == '3': #Download bridge's information
            gm.show_metrics(gcookie)
        elif mode == '4': #Download bridge's information
            gm.dl_bridgemetric(gcookie)

        mode = raw_input('>>> ')
        if mode == '1': #Output Raw JSON of a camera's informtaion.
            devicelisto()
        elif mode == '2': #Export CSV of current user's device list.
            devicelistcsvo()
        else:
            break

