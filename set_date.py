import datetime

def datecheck(date_str) :
    try :
        date_formatted = datetime.datetime.strptime(date_str, "%Y/%m/%d %H:%M:%S")
        print(date_formatted)
        return(date_formatted)
    except ValueError:
        print("Date format error!")
        return None

def inputST():
    ST = raw_input('start time (YYYY/MM/DD HH:MM:SS) >>> ')
    STd = datecheck(ST)
    STs = sTd2STs(STd)
    return(STs)

def inputET():
    ET = raw_input('end time (YYYY/MM/DD HH:MM:SS) >>> ')
    ETd = datecheck(ET)
    ETs = eTd2ETs(ETd)
    return(ETs)

def sTd2STs(STd):
    try:
        ST_UTC = STd - datetime.timedelta(hours = 9)
#        ST_JSTs = STd.strftime("%Y%m%d%H%M%S")
        ST_UTCs = ST_UTC.strftime("%Y%m%d%H%M%S")
        return(ST_UTCs)
    except:
        return None

def eTd2ETs(ETd):
    try:
        ET_UTC = ETd - datetime.timedelta(hours = 9)
#        ET_JSTs = ETd.strftime("%Y%m%d%H%M%S")
        ET_UTCs = ET_UTC.strftime("%Y%m%d%H%M%S")
        return(ET_UTCs)
    except:
        return None
