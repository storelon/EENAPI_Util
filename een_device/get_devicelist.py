import json
import requests
import sys, os

sys.path.append(os.getcwd())

from een_filer import export as xd
from een_localize import language

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

def devicelist(gcookie):
    '''
    Menu of device list.
    :param string gcookie: current session's cookie.
    '''
    lang = language.Language('een_device/get_devicelist')
    global cookie
    cookie = gcookie
    while True:
        print(lang.getStrings(1).replace('\n',''))
        #1 to output raw JSON
        print(lang.getStrings(2).replace('\n',''))
        #2 to export CSV
        print(lang.getStrings(3).replace('\n',''))
        #0 to return to menu
        mode = raw_input('>>> ')
        if mode == '1': #Output Raw JSON of a camera's informtaion.
            devicelisto()
        elif mode == '2': #Export CSV of current user's device list.
            devicelistcsvo()
        else:
            break

def devicelisto():
    '''
    Send device list to the file writer.
    '''
    xd.fileout(get_devicelist(), 'devicelist')

def devicelistcsvo():
    '''
    Send device list to the CSV maker.
    '''
    strings = [u'type,name,ESN,IP\r\n']

    def nonid(camid): #If the camera ID is None, replace inside of camid to a empty string.
        if camid == None:
            camid = u''
        return camid

    #Appending lines to the list with loops.
    [strings.append(i[3] + u',' + i[2] + u',' + nonid(i[1]) + u',' +
                   i[14].replace(',',';') + u'\r\n') for i in get_devicelist().json()]
    xd.makecsv(strings, 'devicelist')
