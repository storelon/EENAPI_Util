import json
import requests
import export_devicelist as xd

cookie = ''

def make_camlist():
    response = requests.get('https://login.eagleeyenetworks.com/g/device/list?t=camera', cookies=cookie)
    print('<camera list>')
    for i in range(len(response.json())):
        print(response.json()[i][1])
    return response

def get_devicelist():
    response = requests.get('https://login.eagleeyenetworks.com/g/device/list', cookies=cookie)
    print response
    return response

def cameras(gcookie):
    global cookie
    cookie = gcookie
    devicelist = make_camlist()
    camlist = []
    for i in devicelist.json():
        camlist.append(i[1])
    return camlist

def devicelist(gcookie):
    global cookie
    cookie = gcookie
    while True:
        print('1 to output raw JSON, 2 to export CSV, 0 to return to menu.')
        mode = raw_input('>>> ')
        if mode == '1':
            devicelisto()
        elif mode == '2':
            devicelistcsvo()
        else:
            break

def devicelisto():
    xd.fileout(get_devicelist(), 'devicelist')

def devicelistcsvo():
    xd.makecsv(get_devicelist())
