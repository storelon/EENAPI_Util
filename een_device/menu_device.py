import json
import requests
import sys, os

import get_bridge as gb
import get_metric as gm
import get_devicelist as gd

sys.path.append(os.getcwd())

from een_filer import export as xd
from een_localize import language

def menu_bridgeinfo(cookie):
    '''
    Display this package's menu.
    :param string cookie: Current session's cookie.
    '''
    lang = language.Language('een_device/menu_device')
    while True:
        print(lang.getStrings(0).replace('\n',''))
        #1 to display your bridge list (include version information)
        print(lang.getStrings(1).replace('\n',''))
        #2 to download detailed information of the specified bridge
        print(lang.getStrings(2).replace('\n',''))
        #3 to download informations of your devices as a raw JSON file
        print(lang.getStrings(3).replace('\n',''))
        #4 to download and export your device list as a CSV file
        print(lang.getStrings(4).replace('\n',''))
        #5 to display your bridge metrics
        print(lang.getStrings(5).replace('\n',''))
        #6 to download and export your bridge metrics as a CSV file
        print(lang.getStrings(6).replace('\n',''))
        #0 to return to menu
        mode = raw_input('>>> ')
        if mode == '1': #Show bridge list
            gb.show_bridges(cookie)
        elif mode == '2': #Download bridge's information
            gb.dl_bridgeinfo(cookie)
        elif mode == '3': #Output Raw JSON of a camera's informtaion.
            gd.devicelisto(cookie)
        elif mode == '4': #Export CSV of current user's device list.
            gd.devicelistcsvo(cookie)
        elif mode == '5': #Download bridge's information
            gm.show_metrics(cookie)
        elif mode == '6': #Download bridge's information
            gm.dl_bridgemetric(cookie)


        elif mode == '0':
            break

