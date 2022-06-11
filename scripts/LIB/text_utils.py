import os

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
_END = '\033[0m'

def result_text(flg):
    if flg:
        return green_text("AC")
    else:
        return red_text("WA")

def red_text(text):
    return RED + text + _END

def green_text(text):
    return GREEN + text + _END

def yellow_text(text):
    return YELLOW + text + _END

def num2rainbow_text(num):
    return '\033[9' + str((num+5)%6+1) + 'm' + str(num) + _END

PS_CNCT = '\\'
NPS_CNCT = '/'
if os.name == 'nt':
    PS_CNCT = '\\'
    NPS_CNCT = '/'
elif os.name == 'posix':
    PS_CNCT = '/'
    NPS_CNCT = '\\'

def path_correct(path):
    return PS_CNCT.join(path.split(NPS_CNCT))
