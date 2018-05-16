import json
import requests
import sys
import codecs

import operate_dir as od

def fileout(givenlist, filename):
    dirname = 'output'
    dirname = od.createdir(dirname) #Prepare for failure of making directory
    try:
        with codecs.open(dirname + '/' + filename + '.txt', 'w', 'utf_8') as f:
            json.dump(givenlist.json(), f, ensure_ascii=False, encoding='utf8', indent=4, )

        with open(dirname + '/' + filename + '.txt', 'r', ) as f:
            Allf = f.read()

        Allf.replace('\n', '\r\n')
    
        with open(dirname + '/' + filename + '.txt', 'w') as f:
            f.write(Allf)

        print('File outputed.')
    except IOError:
        print('File output error!!!')
    except:
        print('Unknown error!!!')

def makecsv(devicelist):
    string = [u'type,name,ESN,IP\r\n']
    for i in devicelist.json():
        if i[1] == None:
            i[1] = u''
        i[14] = i[14].replace(',', ';')
        string.append(i[3] + u',' + i[2] + u',' + i[1] + u',' + i[14] + u'\r\n')
    dirname = 'output'
    dirname = od.createdir(dirname) #Prepare for failure of making directory

    try:
        with codecs.open(dirname + '/' + 'devicelist.csv', 'w', 'utf_8') as f:
            f.writelines(string)
        print('File outputed.')
    except IOError:
        print('File output error!!!')
        sys.exit()
    except:
        print('Unknown error!!!')
        sys.exit()
