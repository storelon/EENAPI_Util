import requests
import sys, os
import json
import codecs
import datetime

import get_bridge as gb

sys.path.append(os.getcwd())

from een_filer import operate_dir as od
from een_localize import language
from een_filer import export
from een_account import get_account as ga
from een_account import set_account as sa
from een_date import set_date as sd

gcookie = ''

def get_bridgemetric(bridge):
    '''
    Get specified bridge's metrics.
    :param string bridge: Bridge id.
    :return json response: Specified bridge's metrics.
    '''
    response = requests.get('https://login.eagleeyenetworks.com/g/metric/bridgebandwidth',
                            {'id':bridge}, cookies=gcookie)
    return(response)

def show_metrics(cookie):
    '''
    Display bridges's metrics which the current account has.
    :param string cookie: Current session's cookie.
    '''
    
    global gcookie
    gcookie = cookie
    
    def printer(string): #printer
        print(string)

    def metrics(bridge):
        a = get_bridgemetric(bridge).json()['core']
        return('Checked date: ' +
               a[-1][0] +
               '\r\ntotal disk space: ' + str(a[-1][1]) +
               'KibiBytes\r\nfree disk space(average): ' +
               str(a[-1][2]) +
               'KibiBytes\r\nused disk space(average): ' +
               str(a[-1][1] - a[-1][2]) + 'KibiBytes\r\n' +
               str(a[-1][3]) + 'Bytes stored, \r\n' +
               str(a[-1][4]) + 'Bytes shaped, \r\n' +
               str(a[-1][5]) + 'Bytes streamed, \r\n' +
               str(a[-1][6]) + 'Bytes freed')

    [printer(i[2] +
             u' (ID: ' +
             i[1] +
             u' ) : metric:\r\n' +
             metrics(i[1])) for i in gb.make_bridgelist(gcookie).json() if metrics(i[1]) != None] #[8][8]

def dl_bridgemetric(cookie):
    #This method will be joint into a common method.
    '''
    Download bridge's metrics and export to a CSV file.
    :param string cookie: Current session's cookie.
    '''
    lang = language.Language('een_device/get_metric')
    global gcookie
    gcookie = cookie
    
    def printer(string): #printer
        print(string)

    def metrics(bridge):
        try:
            m = get_bridgemetric(bridge).json()
            bri_info = gb.get_device(bridge, gcookie).json()['camera_info']
            a = m['core']
            b = m['bandwidth']
            sumb = 0
            length = 0
            aveb = 0
            for bi in b:
                sumb += bi[1]
                length += 1
            if length != 0:
                aveb = sumb / length
            try:
                r = (sd.string2DateTime(a[-1][0]).strftime('%Y/%m/%d %H:%M:%S') +
                     ',' +
                     str(a[-1][1] / (1024**2)) + ',' +
                     str(a[-1][2] / (1024**2)) + ',' +
                     str((a[-1][1] - a[-1][2]) / (1024**2)) + ',' +
                     str(a[-1][5] / (1024**2)) + ',' +
                     str(a[-1][4] / (1024**2)) + ',' +
                     str(aveb * 8 / (1024**2)) + ',' +
                     bri_info[u'version'] + ',')
            except:
                r = (sd.string2DateTime(a[-1][0]).strftime('%Y/%m/%d %H:%M:%S') +
                     ',' +
                     str(a[-1][1] / (1024**2)) + ',' +
                     str(a[-1][2] / (1024**2)) + ',' +
                     str((a[-1][1] - a[-1][2]) / (1024**2)) + ',' +
                     str(a[-1][5] / (1024**2)) + ',' +
                     str(a[-1][4] / (1024**2)) + ',' +
                     str(aveb * 8 / (1024**2)) + ',' +
                     '' + ',')
            return(r)
        except ValueError:
            return(u'N/A,,,')

    accounts = ga.subaccountlist(gcookie)
    
    strings = [u'subaccount name,subaccount id,bridgename,bridgeID,' +
               'last check date,total disk space(GiB),average free disk space(GiB),' + 
               'average used disk space(GiB),MebiBytes streamed,MebiBytes shaped,Cloud BM Measured(Mbps),Firmware Version\r\n']

    #Current account's bridges.
    [strings.append('(Current account),,' +
                    i[2] + u',' + i[1] + u',' +
                    metrics(i[1]) +
                    u'\r\n') for i in gb.make_bridgelist(gcookie).json() if metrics(i[1]) != None] #[8][8] #401deru


    #Subaccounts bridges.
    def loop(j):
        print(lang.getStrings(3).replace('\n','') + j.encode('utf-8'))
        #Changing to subaccount: 
        sa.set_account(j,cookie)
        [strings.append(accounts[1][accounts[0].index(j)] +
                        u',' + j + u',' + i[2] + u',' + i[1] + u',' +
                        metrics(i[1]) +
                        u'\r\n') for i in gb.make_bridgelist(gcookie).json() if metrics(i[1]) != None] #[8][8]
        sa.reset_account(cookie)

        
    if accounts != None:
        [loop(j) for j in accounts[0]]
    filer = export.Filer()
    filer.fileout(strings, 'bridgemetrics')
