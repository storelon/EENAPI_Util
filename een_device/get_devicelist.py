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
    Get a camera list.
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
    Get a device list which current user have.
    :return json response: A raw device list.
    '''
    
    response = requests.get('https://login.eagleeyenetworks.com/g/device/list', cookies=cookie)
    print response
    return response

def cameras(gcookie):
    '''
    Extract camera ID from a JSON.
    :param string gcookie: Current session's cookie.
    :return array camlist: Array of camera ID list.
    '''
    global cookie
    cookie = gcookie
    camlist = []
    [camlist.append(i[1]) for i in make_camlist().json()]
    return camlist

def devicelisto(gcookie):
    '''
    Send a device list to the file writer.
    :param string gcookie: Current session's cookie.
    '''
    global cookie
    cookie = gcookie
    filer = export.Filer()
    filer.fileout(get_devicelist(), 'devicelist')

def devicelistcsvo(gcookie):
    #This method will be joint into a common method.
    '''
    Get and make a device list and convert to CSV format.
    And this method check to sub account's devices if current account has sub account.
    Send device list to the CSV maker.
    :param string gcookie: Current session's cookie.
    '''
    global cookie
    cookie = gcookie
    lang = language.Language('een_device/get_devicelist')

    keylist = [u'camera_property_model',u'bridge',u'camera_state_version',u'intf',
               u'tagmap_status_state',u'camera_property_make',u'camera_retention_asset',u'camera_newest',u'camera_oldest',u'connect',
               u'uuid',u'service',u'camera_retention_etag',u'make',u'ipaddr',u'ts',u'r_model',u'version',u'admin_password',u'esn',u'status',
               u'admin_user',u'r_make',u'camera_property_version',u'r_version',u'mac',u'register_id',u'bridgeid',u'now',u'camera_property_analog',
               u'class',u'status_hex',u'camera_retention_interval',u'camera_now',u'camera_abs_newest',u'camera_abs_oldest',u'camera_valid_ts',
               u'model',u'camtype',u'proxy']

    #Prepare list of lines which will be wrote.
    strings = [u'account_name,account_id,type,name,' + ','.join(keylist) + ',Number of Attached cameras']

    #Check Subaccounts.
    accounts = ga.subaccountlist(cookie)

    #Appending current acount's devices to the list.
    [strings.append(x) for x in [stringer(i, '(Current account),,', keylist) for i in get_devicelist().json()]]


    #Appending subaccount's devices to the list.
    def subaccountdig(j):
        print(lang.getStrings(1).replace('\n','') + j.encode('utf-8'))
        #Changing to subaccount: 
        sa.set_account(j, cookie)
        [strings.append(x) for x in [stringer(i, accounts[1][accounts[0].index(j)] + u',' + j + u',', keylist) for i in get_devicelist().json()]]
        sa.reset_account(cookie)


    if accounts != None:
        [subaccountdig(j) for j in accounts[0]]

    strings = number_of_cameras(strings)

    #Export to a file.
    filer = export.Filer()
    filer.fileout(strings, 'devicelist')


def stringer(i, j, keylist):
    '''
    Make strings for Strings List for CSV
    :param list i: A list of devices.
    :param list j: Head of the csv records. Keys of the account name and the account ID.
    :param list keylist: A key list of the device informations for the CSV.
    :return string: strings of a record for the CSV
    '''
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
    
    return(j + i[3].replace(',',';') + u',' + i[2].replace(',',';') + k)

def number_of_cameras(strings):
    '''
    Compute number of cameras from the CSV strings.
    :param list strings: A list of strings to be wrote in the CSV file.
    :return strings2: strings of a record for the CSV
    '''
    def checknum(bridgeid, accountid):
        num = 0
        for line in strings:
            list_line = line.split(',')
            if list_line[5] == bridgeid and list_line[1] == accountid and list_line[5] != '':
                num += 1
        return(num)
    
    strings2 = []
    
    for line in strings:
        if ',bridge,' in line and strings.index(line) > 0:
            list_line = line.split(',')
            num = checknum(list_line[14], list_line[1])
            strings2.append(strings[strings.index(line)] + ',' + str(num) + u'\r\n')
        else:
            strings2.append(strings[strings.index(line)] + ',' + u'\r\n')

    return(strings2)
