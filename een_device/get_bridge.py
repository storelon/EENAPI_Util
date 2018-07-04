import requests
import sys, os
import json
import codecs

import get_metric as gm

sys.path.append(os.getcwd())

from een_filer import operate_dir as od
from een_filer import export
from een_localize import language

gcookie = ''

def get_bridge(bridge):
    '''
    Get specified bridge's informations.
    :param string bridge: Bridge id.
    :return json response: Specified bridge's informations.
    '''
    response = requests.get('https://login.eagleeyenetworks.com/g/device', {'id':bridge}, cookies=gcookie)
    return(response)

def make_bridgelist(cookie):
    '''
    Get bridge list.
    :return json response: Raw bridge list.
    '''
    response = requests.get('https://login.eagleeyenetworks.com/g/device/list?t=bridge', cookies=cookie)
    print(response)
    return response

def dl_bridgeinfo(cookie):
    '''
    Get bridge information and write it a file.
    '''
    global gcookie
    gcookie = cookie

    lang = language.Language('een_device/get_bridge')
    bridge = raw_input(lang.getStrings(3).replace('\n',''))
    #Bridge ID >>> 
    bridgeinfo = get_bridge(bridge)
    print(bridgeinfo)
    if bridgeinfo.status_code == 200: #Completely got bridge information.
        filer = export.Filer()
        filer.fileout(bridgeinfo, 'bridge_' + bridge)
    else:
        print(lang.getStrings(4).replace('\n',''))
        #Unknown bridge.

def show_bridges(cookie):
    '''
    Get list of bridges witch current account has and the bridges version.
    '''
    global gcookie
    gcookie = cookie
    
    def printer(string): #printer
        print(string)
    
    [printer(i[2] + u' (ID: ' + i[1] + u' ) : version ' +
             get_bridge(i[1]).json()['camera_info']['camera_property_version'] ) for i in make_bridgelist(cookie).json()] #[8][8]


