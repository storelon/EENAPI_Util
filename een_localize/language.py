# -*- coding: utf-8 -*-
import os, sys

class Language:
    '''
    Language localizing class.
    Read 'Lang' file to set localize option.
    Inside of 'Lang' file:
        ja: Set to Japanese.
        en: Set to English.
    '''

    def getStrings(self, num):
        '''
        Get localized text from the initiated array.
        :param integer num: Number of text (zero based indexed).
        :return string: Return text from localized texts.
        '''
        
        return self.strings[num]

    def setLang(self):
        '''
        Get language setting from 'Lang' file.
        :return 
        '''
        try: #Trying to opening the file.
            with open('lang', 'r') as f:
                lang = f.read()
        except IOError:
            print('Localized option cannot open!!!')
            sys.exit()
        except:
            print('Localized option cannot open for unknown reason!!!')
            sys.exit()
        return lang
    
    def __init__(self, module):
        '''
        Initial method.
        :param string module: Module name for localized text file path.
        '''
        lang = self.setLang()
        self.strings = []
        try: #Trying to open localized text file.
            with open('een_localize/' + module + '.' + lang, 'r') as f: 
                [self.strings.append(x) for x in f.readlines()]
        except IOError:
            try:
                with open('een_localize/' + module + '.en', 'r') as f: 
                    [self.strings.append(x) for x in f.readlines()]            
            except:
                print('Cannot open localized text file!!!')
                sys.exit()
        except:
            print('Cannot open localized text file for unknown reason!!!')
            sys.exit()
