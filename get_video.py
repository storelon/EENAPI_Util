import requests
import json
import pprint
import auth
import os
import shutil

import set_date as sd
import operate_dir as od

def make_url(videotimelist, camid) :
    url = []
    for i in videotimelist.json():
        url.append('https://login.eagleeyenetworks.com/asset/play/video.flv?id=' + camid + ';start_timestamp=' + i['s'] + ';' + 'end_timestamp=' + i['e'])
    return url

def get_videotimelist(camid, STs , ETs, cookie) :
    query = 'https://login.eagleeyenetworks.com/asset/list/video?start_timestamp=' + STs + '.000;end_timestamp=' + ETs + '.000;id=' + camid + ';options=coalesce'
    response = requests.get(query, cookies=cookie)
    print(response)
    if response.status_code == 200 and not response.json() == []:
        return(response)
    elif response.status_code == 400:
        print(camid + ': The camera isn\'t exist in specified time range.')
        print('Error : ' + str(response.status_code))
    elif response.json() == []:
        print(camid + ': No video found in specified time range.')


def video_download(camid, STd, ETd, cookie):
    try:
        videotimelist = get_videotimelist(camid, STd, ETd, cookie)
    except:
        print('Maybe invalid camera ID.')
        raise TypeError
    dirname = 'camera_' + camid
    dirname = od.createdir(dirname)
    try:
        url = make_url(videotimelist, camid)
        j = 0
        for i in url:
            file_name = dirname + '/' + camid + '_' + videotimelist.json()[j]['s'] + '.flv'
            print('Downloading > ' + i)
            response = requests.get(i, cookies = cookie, stream = True)
            if response.status_code == 200:
                with open(file_name, 'wb') as file :
                    response.raw.decode_content = True
                    shutil.copyfileobj(response.raw, file)
                    print('Downloaded.')
            else:
                print('Response error!!')
                print(resopnse.status_code)
            j += 1
        print(camid + '\'s videos download complete.')
    except AttributeError:
        print('Download canceled.')
    except:
        print('Unknown error!!!')
