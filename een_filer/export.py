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

def makecsv(listing, filename): # will be for generic use (3 param for filename,header,list)
    '''
    Create a CSV file from given device list.
    :param json devicelist: Raw JSON of device list.
    '''
    lang = language.Language('een_filer/export')

    dirname = 'output'
    dirname = od.createdir(dirname) #Prepare for failure of making directory

    try: #Trying to write a file.
        with codecs.open(dirname + '/' + filename + '.csv', 'w', 'utf_8') as f:
            f.writelines(listing)
        print(lang.getStrings(0).replace('\n',''))
        #File outputed.
    except IOError:
        print(lang.getStrings(1).replace('\n',''))
        #File output error!!!
    except:
        print(lang.getStrings(2).replace('\n',''))
        import traceback
        traceback.print_exc()
        #Unknown error!!!
