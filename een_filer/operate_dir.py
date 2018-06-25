import os, sys

sys.path.append(os.getcwd())

from een_localize import language

def createdir(dirname):
    '''
    Simply create a directory.
    :param string dirname: the directory's name.
    '''
    lang = language.Language('een_account/operate_account')
    try:
        if not os.path.exists(dirname):
            os.mkdir(dirname)
    except:
        print(lang.getStrings(0).replace('\n',''))
        dirname = '.'
    return(dirname)
