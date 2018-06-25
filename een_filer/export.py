import json
import requests
import sys, os
import codecs

import operate_dir as od

sys.path.append(os.getcwd())

from een_localize import language

def fileout(givenlist, filename):
    '''
    Make a file from given argument.
    Let line feed code adapt to Windows.
    :param json givenlist: JSON which will be writen in the file.
    :param string filename: the file's name.
    '''
    lang = language.Language('een_filer/export')
    dirname = 'output'
    dirname = od.createdir(dirname) #Prepare for failure of making directory
    
    try: #Trying to write a file.
        with codecs.open(dirname + '/' + filename + '.txt', 'w', 'utf_8') as f:
            json.dump(givenlist.json(), f, ensure_ascii=False, encoding='utf8', indent=4, )

        with open(dirname + '/' + filename + '.txt', 'r', ) as f:
            Allf = f.read()

        Allf.replace('\n', '\r\n')
    
        with open(dirname + '/' + filename + '.txt', 'w') as f:
            f.write(Allf)

        print(lang.getStrings(0).replace('\n',''))
        #File outputed.
    except IOError:
        print(lang.getStrings(1).replace('\n',''))
        #File output error!!!
    except:
        print(lang.getStrings(2).replace('\n',''))
        #Unknown error!!!

def makecsv(devicelist):
    '''
    Create a CSV file from given device list.
    :param json devicelist: Raw JSON of device list.
    '''
    lang = language.Language('een_filer/export')
    string = [u'type,name,ESN,IP\r\n']

    def nonid(camid): #If the camera ID is None, replace inside of camid to a empty string.
        if camid == None:
            camid = u''
        return camid

    #Appending lines to the list with loops.
    [string.append(i[3] + u',' + i[2] + u',' + nonid(i[1]) + u',' +
                   i[14].replace(',',';') + u'\r\n') for i in devicelist.json()]
    dirname = 'output'
    dirname = od.createdir(dirname) #Prepare for failure of making directory

    try: #Trying to write a file.
        with codecs.open(dirname + '/' + 'devicelist.csv', 'w', 'utf_8') as f:
            f.writelines(string)
        print(lang.getStrings(0).replace('\n',''))
        #File outputed.
    except IOError:
        print(lang.getStrings(1).replace('\n',''))
        #File output error!!!
    except:
        print(lang.getStrings(2).replace('\n',''))
        #Unknown error!!!
