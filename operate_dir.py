import os

def createdir(dirname):
    try:
        if not os.path.exists(dirname):
            os.mkdir(dirname)
    except:
        print('Cannot create directory.')
        dirname = '.'
    return(dirname)
