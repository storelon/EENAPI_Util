import requests
import sys, os
import json
import codecs

import get_metric as gm

sys.path.append(os.getcwd())

from een_filer import operate_dir as od
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

def fileout(bridgename, bridgeinfo):
    '''
    File writer method. Make a JSON formated file from given bridge name and informations.
    :param string bridgename: Specified bridge ID. will be file name.
    :param json bridgeinfo: Bridge informations. will be the file's content.
    '''
    lang = language.Language('een_device/get_bridge')

    dirname = 'output'
    dirname = od.createdir(dirname) #Prepare for failure of making directory
    try: #Try to write a file.
        with codecs.open(dirname + '/bridge_' + bridgename + '.txt', 'w', 'utf_8') as f:
            json.dump(bridgeinfo.json(), f, ensure_ascii=False, encoding='utf8', indent=4, )

        with open(dirname + '/bridge_' + bridgename + '.txt', 'r', ) as f:
            Allf = f.read()

        Allf.replace('\n', '\r\n')
    
        with open(dirname + '/bridge_' + bridgename + '.txt', 'w') as f:
            f.write(Allf)

        print(lang.getStrings(0).replace('\n',''))
        #File outputed.
    except IOError: #File writing failure.
        print(lang.getStrings(1).replace('\n',''))
        #File output error!!!
    except: #Expect failure.
        print(lang.getStrings(2).replace('\n',''))
        #Unknown error!!!

def make_bridgelist():
    '''
    Get bridge list.
    :return json response: Raw bridge list.
    '''
    response = requests.get('https://login.eagleeyenetworks.com/g/device/list?t=bridge', cookies=gcookie)
    print(response)
    return response

def dl_bridgeinfo():
    '''
    Get bridge information and write it a file.
    '''
    lang = language.Language('een_device/get_bridge')
    bridge = raw_input(lang.getStrings(3).replace('\n',''))
    #Bridge ID >>> 
    bridgeinfo = get_bridge(bridge)
    print(bridgeinfo)
    if bridgeinfo.status_code == 200: #Completely got bridge information.
        fileout(bridge, bridgeinfo)
    else:
        print(lang.getStrings(4).replace('\n',''))
        #Unknown bridge.

def show_bridges():
    '''
    Get list of bridges witch current account has and the bridges version.
    '''
    
    def printer(string): #printer
        print(string)
    
    [printer(i[2] + u' (ID: ' + i[1] + u' ) : version ' +
             get_bridge(i[1]).json()['camera_info']['camera_property_version'] ) for i in make_bridgelist().json()] #[8][8]

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
        print(lang.getStrings(8).replace('\n',''))
        #3 to display bridge metrics
        print(lang.getStrings(9).replace('\n',''))
        #4 to bridge metrics to export CSV
        print(lang.getStrings(7).replace('\n',''))
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
        elif mode == '0': #Return to menu
            break
