import json
import requests
import sys, os
import codecs

import operate_dir as od

sys.path.append(os.getcwd())

from een_localize import language

class Filer:
    '''
    File writer class.
    methods:
    __init__: init the file name and directory name.
    __responsewriter: write given content to file if the content is JSON.
    __listwriter: write given content to file if the content is list formated.
    fileout: This class's the only accessible method. decide the given content is list or JSON.
    '''

    
    def __init__(self):
        self.filename = ''
        self.dirname = ''

    def __responsewriter(self, content):
        '''
        Write content to the file.
        Let the line feed code adapt to Windows.
        :param json content: JSON which will be writen in the file.
        '''
        with codecs.open(self.dirname + '/' + self.filename + '.txt', 'w', 'utf_8') as f:
            json.dump(content.json(), f, ensure_ascii=False, encoding='utf8', indent=4, )

        with open(self.dirname + '/' + self.filename + '.txt', 'r', ) as f:
            Allf = f.read()

        Allf.replace('\n', '\r\n')

        with open(self.dirname + '/' + self.filename + '.txt', 'w') as f:
            f.write(Allf)

    def __listwriter(self, content):
        '''
        Write content to the file.
        :param list content: list which will be writen in the file.
        '''
        with codecs.open(self.dirname + '/' + self.filename + '.csv', 'w', 'utf_8') as f:
            f.writelines(content)
    
    def fileout(self, content, gfilename):
        '''
        Make a file from given argument.
        Accept either JSON or list and write it to a file.
        This will accept more format if it necessary in future.
        :param content: This will be content of writen file. it's either JSON or list.
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
