import json
import requests

import operate_dir as od
import export_devicelist as xd

cookie = ''

def get_accountlist():
    response = requests.get('https://login.eagleeyenetworks.com/g/account/list', cookies=cookie)
    print(response)
    return(response)

def accountlist(gcookie):
    global cookie
    cookie = gcookie
    accounts = get_accountlist()
    for i in accounts.json():
        print(i[1] + ' (ID: ' + i[0] + ' )')

def dl_accountlist(gcookie):
    global cookie
    cookie = gcookie
    accounts = get_accountlist()
    xd.fileout(accounts, 'subaccountlist')
    
