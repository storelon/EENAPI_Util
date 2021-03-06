import requests
import json
import os, sys
import shutil
import threading
from time import sleep


sys.path.append(os.getcwd())

from een_date import set_date as sd
from een_filer import operate_dir as od
from een_localize import language

def make_url(videotimelist, camid) :
    '''
    Make download URL from given video time list.
    :param json videotimelist: The video's start time and end time.
    :param string camid: The specified camera's ID.
    :return string url: The download URL.
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
    '''
    Get and make a list of time that the specified camera's video in the specified period exists.
    :param string camid: The specified camera's ID.
    :param string STs: Start date time of the period.
    :param string ETs: End date time of the period.
    :param string cookie: Current session's cookie.
    :return JSON response: A response of EEN API include the video's start time and end time lists.
    '''
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
    '''
    Download all videos in the specified camera in the specified period,
    With multi threading.
    :param string camid: Specified camera's ID
    :param string STs: Start date time of specified period.
    :param string ETs: End date time of specified period.
    :param string cookie: Current session's cookie.
    '''
    lang = language.Language('een_video/get_video')
    try:
        videotimelist = get_videotimelist(camid, STd, ETd, cookie)
    except:
        print(lang.getStrings(3).replace('\n',''))
        raise TypeError
    dirname = 'camera_' + camid
    dirname = od.createdir(dirname)
    if videotimelist == None:
        print(lang.getStrings(8).replace('\n',''))
        return 0

    #Number of threads.
    thread_num = 4

    url = make_url(videotimelist, camid)
    dlinfo = [dirname, camid, videotimelist, url, cookie]


    spurl = divideurl(url, thread_num)

    #Multi threading
    threads = []
    [threads.append(MyThread("Thread-{}".format(spurl.index(iurl)), iurl, dlinfo)) for iurl in spurl]
    for th in threads:
        th.start()
        sleep(1)
    [th.join() for th in threads]
    
    print(camid.encode('utf-8') + lang.getStrings(7).replace('\n',''))

def divideurl(listing, n):
    '''
    Divide the given video URL list into the given number.
    This method is for multi thread downloading.
    :param list listing: Video URL list.
    :param integer n: Divisor.
    :return string spurl: Divided list such as [[url1,url4][url2,url5][url3,url6]].
    '''
    spurl = [[]]
    [spurl.append([]) for x in range(n - 1)]
    counter = Counter()

    def incri(i):
        '''
        :param integer i: Array's number.
        '''
        try:
            spurl[i].append(listing[counter.getter()])
            print listing[counter.getter()]
            counter.incrementer()
        except:
            pass
    
    num = len(listing)/n
    if len(listing)%n > 0:
        num += 1
    
    [[incri(i) for i in range(n) ] for j in range(num)]
    return spurl
    
class MyThread(threading.Thread):
    '''
    __init__: Initialize member variables.
    run: Set file name and run filedl method.
    filedl: Access the specified url and get a video file. The got file let to send to a member variable.
    fileout: A member
    '''
    def __init__(self, name, url, dlinfo):
        threading.Thread.__init__(self)
        self.dlinfo = dlinfo
        self.url = url
        self.cookie = dlinfo[4]
        self.response = ''
    def run(self):
        for iurl in self.url:
            file_name = self.dlinfo[0] + '/' + self.dlinfo[1] + '_' + self.dlinfo[2].json()[self.dlinfo[3].index(iurl)]['s'] + '.flv'
            self.filedl(iurl, file_name)
        
    def filedl(self, iurl, file_name):
        lang = language.Language('een_video/get_video')
        
        try:
            print(lang.getStrings(6).replace('\n','') + iurl.encode('utf-8'))
            self.response = requests.get(iurl, cookies = self.cookie, stream = True)
            self.fileout(file_name)
        except AttributeError:
            print(lang.getStrings(8).replace('\n',''))

        except:
            print(lang.getStrings(9).replace('\n',''))
            
    def fileout(self, file_name):
        lang = language.Language('een_video/get_video')
        if self.response.status_code == 200:
            with open(file_name, 'wb') as file :
                self.response.raw.decode_content = True
                shutil.copyfileobj(self.response.raw, file)
                print(lang.getStrings(4).replace('\n',''))
        else:
            print(lang.getStrings(5).replace('\n',''))
            print(self.response.status_code),

class Counter():
    def __init__(self):
        self.k = 0

    def incrementer(self):
        self.k += 1

    def getter(self):
        return self.k
