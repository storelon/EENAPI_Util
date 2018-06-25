import sys, os

import get_video as gv

sys.path.append(os.getcwd())

from een_date import set_date as sdt
from een_device import get_devicelist as gd
from een_localize import language

def downloadvideos(cookie) :
    '''
    Download videos with get_video module.
    :param string cookie: Current session's cookie.
    '''
    lang = language.Language('een_video/dl_videos')
    camera = raw_input(lang.getStrings(0).replace('\n',''))
    #Enter camera id or ALL >>> 
    if camera == 'ALL': #Download current user's all camera's videos.
        camlist = gd.cameras(cookie)
    else: #Download specified camera's videos.
        camlist = [camera]
    try: #Trying to download videos.
        STs = sdt.inputST()
        ETs = sdt.inputET()
        if STs == None or ETs == None: #The specified period has wrong.
            raise TypeError
        print(lang.getStrings(1).replace('\n',''))
        #Go download.
        [gv.video_download(i, STs, ETs, cookie) for i in camlist]
    except:
        print(lang.getStrings(2).replace('\n',''))
        #Some error occured. Cannot download.
