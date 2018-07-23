import datetime
import sys, os

sys.path.append(os.getcwd())

from een_localize import language


def datecheck(date_str) :
    '''
    Given strings of specified date to check and format to datetime format.
    :param string date_str: Strings of specified date.
    :return datetime date_formatted: formated date.
    :return None None: Format failure.
    '''
    
    lang = language.Language('een_date/set_date')
    try : #Try to format.
        date_formatted = datetime.datetime.strptime(date_str, "%Y/%m/%d %H:%M:%S")
        print(date_formatted)
        return(date_formatted)
    except ValueError: 
        print(lang.getStrings(0).replace('\n',''))
        #Date format error!
        return None

#inputST() and inputET() will be jointed.
def inputST():
    '''
    Accept input of beginning time of the period.
    :return string: strings of beginning of the period for API's URL.
    '''
    
    lang = language.Language('een_date/set_date')
    return(sTd2STs(datecheck(raw_input(lang.getStrings(1).replace('\n','')))))
    #start time (YYYY/MM/DD HH:MM:SS) >>> 

def inputET():
    '''
    Accept input of end time of the period.
    :return string: strings of end of the period for API's URL.
    '''
    
    lang = language.Language('een_date/set_date')
    return(eTd2ETs(datecheck(raw_input(lang.getStrings(2).replace('\n','')))))
    #end time (YYYY/MM/DD HH:MM:SS) >>>

#sTd2STs() and eTd2ETs will be jointed.
def sTd2STs(STd):
    '''
    Given start time to be substracted 9 hours and convert to a string.
    :param datetime STd: Given time.
    :return datetime ST_UTCs: 9 hours substracted start time.
    :return none: The substraction failed.
    '''
    
    try: #Try to substraction.
        ST_UTC = STd - datetime.timedelta(hours = 9)
#        ST_JSTs = STd.strftime("%Y%m%d%H%M%S")
        ST_UTCs = ST_UTC.strftime("%Y%m%d%H%M%S")
        return(ST_UTCs)
    except:
        return None

def eTd2ETs(ETd):
    '''
    Given end time to be substracted 9 hours and convert to a string.
    :param datetime ETd: Given time.
    :return datetime ET_UTCs: 9 hours subtracted end time.
    :return none: The substraction failed.
    '''
    
    try: #Try to substraction.
        ET_UTC = ETd - datetime.timedelta(hours = 9)
#        ET_JSTs = ETd.strftime("%Y%m%d%H%M%S")
        ET_UTCs = ET_UTC.strftime("%Y%m%d%H%M%S")
        return(ET_UTCs)
    except:
        return None

def string2DateTime(string):
    '''
    Given strings to be added 9 hours and convert to datetime format.
    :param string string: Given string of time.
    :return datetime: 9 hours added time.
    '''
    
    d = datetime.datetime.strptime(string, '%Y%m%d%H%M%S.000')
    d = d + datetime.timedelta(hours = 9)
    return(d)
