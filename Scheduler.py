import os
import time
import datetime

alarm1 = (1,30,0)
alarm2 = (1,45,0)

def main():
    while (1):
        nowtime = todaytime()
        if nowtime == alarm1:
            alarm1function()
        if nowtime == alarm2:
            alarm1function()
        if nowtime[2] == 0:
            print(nowtime[0],":",nowtime[1],":",nowtime[2])
        time.sleep(1)

def alarm1function():
    os.system("cd c:\code\GitCode\GitCode")
    os.system("git pull https://github.com/WAPE5523/GitCode.git")

def alarm2function():
    os.system("cd c:\code\GitCode\GitCode")
    os.system("StonkScanner.py")

def todaytime():
    date = datetime.datetime.now()
    hour = int(date.hour)
    minute = int(date.minute)
    sec = int(date.second)
    
    nowtime = (hour, minute, sec)
    return nowtime
main()