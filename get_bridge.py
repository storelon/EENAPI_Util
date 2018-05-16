import requests
import sys
import json
import codecs

import operate_dir as od

cookie = ''

def get_bridge(bridge):
    response = requests.get('https://login.eagleeyenetworks.com/g/device', {'id':bridge}, cookies=cookie)
    return(response)

def fileout(bridgename, bridgeinfo):

    dirname = 'output'
    dirname = od.createdir(dirname) #Prepare for failure of making directory
    try:
        with codecs.open(dirname + '/bridge_' + bridgename + '.txt', 'w', 'utf_8') as f:
            json.dump(bridgeinfo.json(), f, ensure_ascii=False, encoding='utf8', indent=4, )

        with open(dirname + '/bridge_' + bridgename + '.txt', 'r', ) as f:
            Allf = f.read()

        Allf.replace('\n', '\r\n')
    
        with open(dirname + '/bridge_' + bridgename + '.txt', 'w') as f:
            f.write(Allf)

        print('File outputed.')
    except IOError:
        print('File output error!!!')
    except:
        print('Unknown error!!!')

def make_bridgelist():
    response = requests.get('https://login.eagleeyenetworks.com/g/device/list?t=bridge', cookies=cookie)
    print(response)
    return response

def dl_bridgeinfo():
    bridge = raw_input('Bridge ID >>> ')
    bridgeinfo = get_bridge(bridge)
    print(bridgeinfo)
    if bridgeinfo.status_code == 200:
        fileout(bridge, bridgeinfo)
    else:
        print('Unknown bridge.')

def show_bridges():
    bridges = make_bridgelist()
    for i in bridges.json():
        bridgeinfo = get_bridge(i[1])
        print(i[2] + ' (ID: ' + i[1] + ' ) : version ' + bridgeinfo.json()['camera_info']['camera_property_version']) #[8][8]

def menu_bridgeinfo(gcookie):
    global cookie
    cookie = gcookie
    while True:
        print('1 to show bridge list, 2 to download bridge\'s infomation ')
        print('0 to return to menu.')
        mode = raw_input('>>> ')
        if mode == '1':
            show_bridges()
        elif mode == '2':
            dl_bridgeinfo()
        elif mode == '0':
            break
