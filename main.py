import auth
import set_date as sdt
import get_devicelist as gd
import dl_videos as dv
import operate_account as oa
import get_account as ga
import get_bridge as gb

def apitool_main():
    cookie = auth.get_cookie()
    while True:
        print('1 to output devicelist, 2 to download videos')
        print('3 to change to subaccount, 4 to output bridge\'s infomations')
        print('9 to exit with logout, 0 to exit without logout.')
        mode = raw_input('>>> ')
        if mode == '1':
            gd.devicelist(cookie)
        elif mode == '2':
            dv.downloadvideos(cookie)
        elif mode == '3':
            oa.menu_account(cookie)
        elif mode == '4':
            gb.menu_bridgeinfo(cookie)
        elif mode == '9':
            auth.logout(cookie)
            print('Exiting.')
            break
        elif mode == '0':
            print('Exiting.')
            break

if __name__ == '__main__':
    apitool_main()
