import requests
import json
import os, sys
import shutil

sys.path.append(os.getcwd())

from een_date import set_date as sd
from een_filer import operate_dir as od
from een_localize import language

def make_url(videotimelist, camid) :
    '''
    Make download URL.
    :param json videotimelist: The video's start time and end time.
    ::
    '''
    url = []
    [url.append('https://login.eagleeyenetworks.com/asset/play/video.flv?id=' +
                camid +
                ';start_timestamp=' +
                i['s'] + ';' +
                'end_timestamp=' +
                i['e']) for i in videotimelist.json()]
    return url

def get_videotimelist(camid, STs , ETs, cookie) :
    lang = language.Language('een_video/get_video')
    query = 'https://login.eagleeyenetworks.com/asset/list/video?start_timestamp=' + STs + '.000;end_timestamp=' + ETs + '.000;id=' + camid + ';options=coalesce'
    response = requests.get(query, cookies=cookie)
    print(response)
    if response.status_code == 200 and not response.json() == []:
        return(response)
    elif response.status_code == 400:
        print(camid.encode('utf-8') + lang.getStrings(0).replace('\n',''))
        print(lang.getStrings(1).replace('\n','') + str(response.status_code).encode('utf-8'))
    elif response.json() == []:
        print(camid.encode('utf-8') + lang.getStrings(2).replace('\n',''))

def video_download(camid, STd, ETd, cookie):
    lang = language.Language('een_video/get_video')
    try:
        videotimelist = get_videotimelist(camid, STd, ETd, cookie)
    except:
        print(lang.getStrings(3).replace('\n',''))
        raise TypeError
    dirname = 'camera_' + camid
    dirname = od.createdir(dirname)

    def fileout(response, file_name):
        if response.status_code == 200:
            with open(file_name, 'wb') as file :
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, file)
                print(lang.getStrings(4).replace('\n',''))
        else:
            print(lang.getStrings(5).replace('\n',''))
            print(resopnse.status_code)

    def filedl(iurl):
        file_name = dirname + '/' + camid + '_' + videotimelist.json()[url.index(iurl)]['s'] + '.flv'
        print(lang.getStrings(6).replace('\n','') + iurl.encode('utf-8'))
        response = requests.get(iurl, cookies = cookie, stream = True)
        fileout(response, file_name)

    try:
        url = make_url(videotimelist, camid)
        [filedl(i) for i in url]
        print(camid.encode('utf-8') + lang.getStrings(7).replace('\n',''))
    except AttributeError:
        print(lang.getStrings(8).replace('\n',''))
    except:
        print(lang.getStrings(9).replace('\n',''))
