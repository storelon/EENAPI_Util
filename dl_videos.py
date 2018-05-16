import get_video as gv
import get_devicelist as gd
import set_date as sdt

def downloadvideos(cookie) :
    camera = raw_input('Enter camera id or ALL >>> ')
    if camera == 'ALL' :
        camlist = gd.cameras(cookie)
    else :
        camlist = [camera]
    
    try:
        STs = sdt.inputST()
        ETs = sdt.inputET()
        if STs == None or ETs == None:
            raise TypeError
        print('Go download.')
        for i in camlist:
            gv.video_download(i, STs, ETs, cookie)
    except:
        print('Some error occured. Cannot download.')
