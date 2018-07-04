import json
import requests
import sys, os
import codecs

import operate_dir as od

sys.path.append(os.getcwd())

from een_localize import language

class Filer:
    def __init__(self):
        self.filename = ''
        self.dirname = ''

    def __responsewriter(self, content):
        with codecs.open(self.dirname + '/' + self.filename + '.txt', 'w', 'utf_8') as f:
            json.dump(content.json(), f, ensure_ascii=False, encoding='utf8', indent=4, )

        with open(self.dirname + '/' + self.filename + '.txt', 'r', ) as f:
            Allf = f.read()

        Allf.replace('\n', '\r\n')

        with open(self.dirname + '/' + self.filename + '.txt', 'w') as f:
            f.write(Allf)

    def __listwriter(self, content):
        with codecs.open(self.dirname + '/' + self.filename + '.csv', 'w', 'utf_8') as f:
            f.writelines(content)
    
    def fileout(self, content, gfilename):
        '''
        Make a file from given argument.
        Let line feed code adapt to Windows.
        :param json givenlist: JSON which will be writen in the file.
        :param string filename: the file's name.
        '''
        lang = language.Language('een_filer/export')
        self.dirname = 'output'
        self.dirname = od.createdir(self.dirname) #Prepare for failure of making directory
        self.filename = gfilename
        try:
            if type(content) is requests.models.Response:
                self.__responsewriter(content)
            elif type(content) is list:
                self.__listwriter(content)
            else:
                raise TypeError
            print(lang.getStrings(0).replace('\n',''))
            #File outputed.
        except IOError:
            print(lang.getStrings(1).replace('\n',''))
            #File output error!!!
        except:
            print(lang.getStrings(2).replace('\n',''))
            #Unknown error!!!
