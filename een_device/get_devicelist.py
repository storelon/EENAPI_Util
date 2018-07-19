import json
import requests
import sys, os

import get_bridge as gb

sys.path.append(os.getcwd())

from een_filer import export
from een_localize import language
from een_account import get_account as ga
from een_account import set_account as sa

cookie = ''

def make_camlist():
    '''
    Get camera list.
    :return json response: JSON which contains camera list.
    '''
    lang = language.Language('een_device/get_devicelist')
    response = requests.get('https://login.eagleeyenetworks.com/g/device/list?t=camera', cookies=cookie)
    print(lang.getStrings(0).replace('\n',''))
    #<camera list>
    
    def printer(string):
        print string
    
    [printer(i[1]) for i in response.json()]
    return response

def get_devicelist():
    '''
    Get device list which current user have.
    :return json response:Raw device list.
    '''
    
    response = requests.get('https://login.eagleeyenetworks.com/g/device/list', cookies=cookie)
    print response
    return response

def cameras(gcookie):
    '''
    Extract camera ID from JSON.
    :return array camlist: Array of camera ID list.
    '''
    global cookie
    cookie = gcookie
    camlist = []
    [camlist.append(i[1]) for i in make_camlist().json()]
    return camlist

def devicelisto(gcookie):
    '''
    Send device list to the file writer.
    '''
    global cookie
    cookie = gcookie
    filer = export.Filer()
    filer.fileout(get_devicelist(), 'devicelist')

def devicelistcsvo(gcookie):
    #This method need to be divided!!!
    '''
    Send device list to the CSV maker.
    '''
    global cookie
    cookie = gcookie

    keylist = [u'camera_property_model',u'bridge',u'camera_state_version',u'intf',
               u'tagmap_status_state',u'camera_property_make',u'camera_retention_asset',u'camera_newest',u'camera_oldest',u'connect',
               u'uuid',u'service',u'camera_retention_etag',u'make',u'ipaddr',u'ts',u'r_model',u'version',u'admin_password',u'esn',u'status',
               u'admin_user',u'r_make',u'camera_property_version',u'r_version',u'mac',u'register_id',u'bridgeid',u'now',u'camera_property_analog',
               u'class',u'status_hex',u'camera_retention_interval',u'camera_now',u'camera_abs_newest',u'camera_abs_oldest',u'camera_valid_ts',
               u'model',u'camtype',u'proxy']
    
    strings = [u'account_name,account_id,type,name,' + ','.join(keylist) + '\r\n']

    #Check Subaccounts.
    accounts = ga.subaccountlist(cookie)

    
    #Appending lines to the list with loops.
    def stringer(i, j):
        try:
            b = gb.get_device(i[1], cookie).json()['camera_info']
        except:
            b = {}
            def appender(x):
                b[u'brank' + str(x)] = ''
            [appender(x) for x in range(40)]
        k = ''

        for c in keylist:
            try:
                k = k + ',' + str(b[c]).replace(',',';')
            except:
                k = k + ','
        
        strings.append(j +i[3] + u',' + i[2] + k + u'\r\n')

    #Appending current acount's devices.
    [stringer(i, '(Current account),,') for i in get_devicelist().json()]


    #Subaccount's bridges.
    def loop(j):
        print(u'Changing to subaccount: ' + j.encode('utf-8'))
        #Changing to subaccount: 
        sa.set_account(j,cookie)
        [stringer(i, accounts[1][accounts[0].index(j)] + u',' + j + u',') for i in get_devicelist().json()]
        sa.reset_account(cookie)

    
    if accounts != None:
        [loop(j) for j in accounts[0]]

    filer = export.Filer()
    filer.fileout(strings, 'devicelist')
