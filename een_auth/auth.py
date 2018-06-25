import json
import requests, requests.utils, pickle
import pprint
import sys
import os
import certifi
from getpass import getpass

sys.path.append(os.getcwd())

from een_localize import language


class Auth:
    '''
    Authorize an Eagle Eye Networks user class.
    Ask user to input username and password.
    If authentication succeed, then store a cookie and its auth key.
    Return cookie when asked auth key per every connection.
    methods:
    __init__: Restore previous cookie and check connection to EEN.
    get_cookie: Return cookie from current Auth instance.
    __set_cookie: Get authorization and set a cookie to current instance.
    __userinput: Ask user for username and password.
    logout: Delete cookie file and request logout.
    __tfa_auth: Request to authorize with two-factor authentication.
    '''
    COOKIEFILE = 'cookie' #cookie file name
    
    
    
    def __init__(self):
        '''
        Restore previous cookie and check connection to EEN.
        :instance_variable json self.cookie: Store the session's cookie.
        '''
        
        #I don't know why but py2exed program wouldn't make cacert.pem
        #Comment out below line if use py2exe.
        #os.environ['REQUESTS_CA_BUNDLE'] = "./certifi/cacert.pem"
        
        self.cookie = ''
        self.lang = language.Language('een_auth/auth')


        #Try to restore cookie from the cookie file. If it failure then login with user input.
        try: #Try to restore.
            with open(Auth.COOKIEFILE, 'r') as f:
                self.cookie = requests.utils.cookiejar_from_dict(pickle.load(f))
            response = requests.get('https://login.eagleeyenetworks.com/g/account/list', cookies=self.cookie)
            if response.status_code != 200:
                print(self.lang.getStrings(0).replace('\n',''))
                #Invalid cookie or the cookie has expired
                raise IncorrectCookieError
        except requests.exceptions.ConnectionError: #The internet connection has fault.
            print(self.lang.getStrings(1).replace('\n',''))
            #Check internet connection!!!
            sys.exit()
        except: #get authentication and authorization.
            self.__set_cookie()

    def get_cookie(self):
        '''
        Return cookie from current Auth instance.
        :return json cookie: Return current session's cookie.
        '''
        return(self.cookie)

    def __set_cookie(self):
        '''
        Get authorization and set a cookie to current instance.
        This method use __userinput method and __TFA_auth method.
        '''
        uid = self.__userinput()
        tfa_bool = False #Initiate TFA option's variable.
        response = requests.post('https://login.eagleeyenetworks.com/g/aaa/authenticate', {'username':uid[0],'password':uid[1]})
        print response        

        try : #Try to set token.
            token = response.json()['token']
        except : #Login failed.
            print(self.lang.getStrings(2).replace('\n',''))
            #Login failure.
            sys.exit()

        if 'two_factor_authentication_code' in response.json() : #The session is requested TFA authentication.
            self.__tfa_auth(response)
            tfa_bool = True

        if tfa_bool == False: #Not necessary TFA and get cookie from EEN then start session.
            response = requests.post('https://login.eagleeyenetworks.com/g/aaa/authorize', {'token':token})
        else: #TFA is necessary. Authentication with TFA numbers.
            tfacode = raw_input(self.lang.getStrings(3).replace('\n',''))
            #Enter the number you received for two factors authentication. >>> 
            response = requests.post('https://login.eagleeyenetworks.com/g/aaa/authorize', {'token':token, 'two_factor_authentication_code': tfacode})
            print(response)
            if response.status_code == 200: #Login success.
                print(self.lang.getStrings(18).replace('\n',''))
                #TFA Login success.
            else: #Login failure.
                print(self.lang.getStrings(19).replace('\n',''))
                #TFA login false.
                sys.exit()

        try: #Save the cookie to disk.
            with open(Auth.COOKIEFILE, 'w') as f:
                pickle.dump(requests.utils.dict_from_cookiejar(response.cookies), f)
        except: #Maybe IO error.
            print(self.lang.getStrings(5).replace('\n',''))
            #Cannot save the cookie...
        self.cookie = response.cookies

    def __userinput(self):
        '''
        Ask user for username and password.
        :return array uid: uid[0] is username, uid[1] is password.
        '''
        uid = ['mail','pass']
        uid[0] = raw_input(self.lang.getStrings(6).replace('\n',''))
        #E-mail adress >>> 
        uid[1] = getpass(self.lang.getStrings(7).replace('\n',''))
        #Password >>> 
        return uid

    def logout(self):
        '''
        Delete cookie file and request logout.
        '''
        response = requests.post('https://login.eagleeyenetworks.com/g/aaa/logout', cookies=self.cookie)
        print response
        if response.status_code == 204: #Logout succeed.
            os.remove(Auth.COOKIEFILE)
            print(self.lang.getStrings(8).replace('\n',''))
            #Logout succeed.
        else: #Logout failure.
            print(self.lang.getStrings(9).replace('\n',''))
            #Error. Logout failure.

    def __tfa_auth(self, response):
        '''
        Request to authorize with two-factor authentication.
        :param json response: Storing TFA's mail address and phone number.
        '''

        while True:
        
            print('E-mail : ' + response.json()['two_factor_authentication_code']['email'])
            print('SMS : ' + response.json()['two_factor_authentication_code']['sms'])

            print(self.lang.getStrings(10).replace('\n',''))
            #1 to send two factor authentication code to E-mail,
            print(self.lang.getStrings(11).replace('\n',''))
            #2 to send the code to SMS.
            tfa_input = raw_input('>>> ')

            if tfa_input == '1': #Request to send TFA code to E-mail address.
                tfamode = 'email'
                print(self.lang.getStrings(12).replace('\n',''))
                #I'll send a number to your E-mail address.
                break
            elif tfa_input == '2': #Request to send TFA code to SMS.
                tfamode = 'sms'
                print(self.lang.getStrings(13).replace('\n',''))
                #I'll send a number to your SMS.
                break
            
        response2 = requests.post('https://login.eagleeyenetworks.com/g/aaa/two_factor_authenticate', {'token':response.json()['token'], 'two_factor_authentication_type':tfamode})
        print(response2)
        
        if response2.status_code == 200: #Succeed.
            print(self.lang.getStrings(16).replace('\n',''))
            #Success to send the code.
        else: #Failed.
            print(self.lang.getStrings(17).replace('\n',''))
            #Failed to send the code.
            sys.exit()
