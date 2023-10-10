import numpy as np
import csv
import robin_stocks
import time
import datetime
from tkinter import *
from matplotlib import pyplot as plt
import gspread
from oauth2client.service_account import ServiceAccountCredentials

tickerlist = [] 
dicts = []
volume = []
dictinitial = {'symbol': 0, 'prevtime': 0, 'currtime': 0, 'deltatimeprev': 0, 'deltatimeccurr': 0, 'prevprice': 0, 'currprice': 0, 'deltaprice': 0, 'delta%/time': 0, 'volprev': 0, 'volcurr': 0, 'deltavolprev': 0, 'deltavolcurr': 0, 'volchange': 0, 'totalvolcheck': 0, '2weekvol': 0}
marketdaytime = 25200
starttime = 0
endtime = 0

pricechangearray = []
pricechangesymbolarray = []
volchangearray = []
volchangesymbolarray = []
totalvolcheckarray = []

#everything until main() is for the gui
window = Tk()
window.title('StonkScanner')

volume = IntVar()
notification = IntVar()
rsivar = IntVar()
holdvol = 0
holdnot = 0
holdrsi = 0

start = datetime.datetime.now()
curr = datetime.datetime.now()
proj = datetime.datetime.now()

volspike = Checkbutton(window, text = 'Volume Tracking', variable = volume, onvalue = 1, offvalue = 0)
volspike.grid(row = 0, column = 3)
rsi = Checkbutton(window, text = 'RSI Tracking', variable = rsivar, onvalue = 1, offvalue = 0)
rsi.grid(row = 1, column = 3)
notif = Checkbutton(window, text = 'Notifications', variable = notification, onvalue = 1, offvalue = 0)
notif.grid(row = 2, column = 3)

currcyctime = Message(window, text = "Current Cycle Runtime:  ")
currcyctime.grid(row = 0, column = 0)
prevcycend = Message(window, text = "Previous Cycle Runtime:  ")
prevcycend.grid(row = 1, column = 0)
nextcycend = Message(window, text = "Projected Next Update")
nextcycend.grid(row = 2, column = 0)

currcyctimeval = Label(window, text = str(datetime.datetime.now()))
currcyctimeval.grid(row = 0, column = 1)
prevcycendval = Label(window, text = str(datetime.datetime.now()))
prevcycendval.grid(row = 1, column = 1)
nextcycendval = Label(window, text = str(datetime.datetime.now()))
nextcycendval.grid(row = 2, column = 1)

currtickertag = Message(window, text = "Current Ticker: ")
currtickertag.grid(row = 4, column = 0)
avgtickertag = Message(window, text = "Average time per ticker:  ")
avgtickertag.grid(row = 5, column = 0)
currstatetag = Message(window, text = "Current State: ")
currstatetag.grid(row = 4, column = 2)
currentstatetimetag = Message(window, text = "Time in Current State:  ")
currentstatetimetag.grid(row = 5, column = 2)

currticker = Label(window, text = "N/A")
currticker.grid(row = 4, column = 1)
avgtickertime = Label(window, text = "Dummy")
avgtickertime.grid(row = 5, column = 1)
currstate = Label(window, text = "Login")
currstate.grid(row = 4, column = 3)
currstatetime = Label(window, text = "Dummy")
currstatetime.grid(row = 5, column = 3)

def main():  
    notfirst = False
    robin_stocks.robinhood.authentication.login('wadepe@yahoo.com', 'Robinhood1!')
    currstate.config(text = 'Importing Tickers')
    window.update()
    tickers('nasdaqtickers.csv')
    tickers('nysetickers.csv')
    dictionarys()
    #for i in dicts:
    #    twoweekavgvol(i)
    print(len(dicts))
    while(True):
        starttime = datetime.datetime.now()
        print('Cycle Start ', starttime)
        clearlists()
        currstate.config(text = 'Updating Symbol Data')
        #window.update()
        for i in dicts:
            updatesymboldata(i, notfirst)
        if notfirst == False:
            notfirst = True
        #holdnot = notification.get()
        #holdrsi = rsivar.get()
        currstate.config(text = 'Writing to Sheet')
        window.update()
        sheetwrite()
        endtime = datetime.datetime.now()
        print('Cycle End ', endtime, '       Difference:  ', endtime - starttime)
        #prevcycendval.config(text = str(starttime))
        #nextcycendval.config(text = str(endtime + endtime - starttime))
        window.update()


    
def clearlists():
    pricechangearray.clear()
    pricechangesymbolarray.clear()
    volchangearray.clear()
    volchangesymbolarray.clear()
    totalvolcheckarray.clear()

def updatecurrprice(infodict):
    #robinhood function to update current ticker price
    hold = robin_stocks.robinhood.stocks.get_latest_price(infodict['symbol'])
    if type(hold[0]) != str:
        print("Nonetype on ticker ", infodict['symbol'])
        print(type(hold[0]))
        return
    infodict['currprice'] = float(hold[0])
    currticker.config(text = infodict['symbol'])
    #currcyctime.config(text = (datetime.datetime.now() - starttime))
    window.update()

def updatecurrvolume(infodict):
    #robinhood function to update current ticker volume
    hold = robin_stocks.robinhood.stocks.get_fundamentals(infodict['symbol'], info='volume')
    if type(hold[0]) != str:
        print("Nonetype on ticker ", infodict['symbol'])
        print(type(hold[0]))
        return
    infodict['currvol'] = float(hold[0])

def twoweekavgvol(infodict):
    hold = robin_stocks.robinhood.stocks.get_fundamentals(infodict['symbol'], info='average_volume_2_weeks')
    if type(hold[0]) != str:
        print("Nonetype on ticker ", infodict['symbol'])
        print(type(hold[0]))
        return
    infodict['2weekvol'] = float(hold[0])

def shiftcurrtoprev(infodict, notfirst):
    #shifts all curr values to prev values in a dictionary before curr is updated
    infodict['prevtime'] = infodict['currtime']
    infodict['prevprice'] = infodict['currprice']
    infodict['deltatimeprev'] = infodict['deltatimecurr']
    infodict['volprev'] = infodict['volcurr']
    infodict['deltavolprev'] = infodict['deltavolcurr']

def updatesymboldata(infodict, notfirst):
    if notfirst:
        shiftcurrtoprev(infodict, notfirst)
    holdvol = volume.get()
    updatecurrprice(infodict)
    if(holdvol):
        updatecurrvolume(infodict)
    infodict['currtime'] = time.time()
    infodict['deltatimecurr'] = infodict['currtime'] - infodict['prevtime']
    infodict['deltavolcurr'] = infodict['volcurr'] - infodict['volprev']
    infodict['deltaprice'] = infodict['currprice'] - infodict['prevprice']
    if notfirst == True:
        if ((infodict['prevprice'] != 0) & (infodict['deltatimecurr'] != 0)):
            infodict['delta%/time'] = (infodict['deltaprice'] / infodict['prevprice']) / infodict['deltatimecurr']
        if(holdvol):
            infodict['volchange'] = (infodict['deltavolcurr'] / infodict['deltatimecurr']) - ((infodict['deltavolprev'] / infodict['deltatimeprev']))
            infodict['totalvolcheck'] = (infodict['2weekvol'] / marketdaytime) - (infodict['volcurr'] / (time.time() - todaytime(7,0,0)))
        


def todaytime(hour, minute, sec):
    date = datetime.datetime.now()
    year = int(date.year)
    month = int(date.month)
    day = int(date.day)
    
    if int(date.strftime("%w")) == 0:
        wday = 6
    else:
        wday = int(date.strftime("%w")) - 1

    yday = int(date.strftime("%j"))
    dst = -1  #if daylight savings time screws with time calculations, this is the culprit
    customtime = (year, month, day, hour, minute, sec, wday, yday, dst)
    return time.mktime(customtime)


def tickers(filename): 
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            check = robin_stocks.robinhood.stocks.get_instruments_by_symbols(row[0], info='tradeable')
            if check == [True]:
                tickerlist.append(row[0])

def flagread():
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open("StonkScanner Flags")
    sheet_instance = sheet.get_worksheet(1)
    print(sheet_instance.col_values(1))

def sheetwrite():
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open("StonkScanner Flags")
    wks2 = sheet.get_worksheet(2)
    wks1 = sheet.get_worksheet(1)
    wks0 = sheet.get_worksheet(0)
    if type(wks2.acell('B1').value == str):
        PriceSpikeVal = float(wks2.acell('B1').value)
    else:
        (print("PriceSpikeVal Issue"))
    if type(wks2.acell('E1').value == str):
        VolSpikeVal = float(wks2.acell('E1').value)
    else:
        (print("VolSpikeVal Issue"))
    sheetarrays(PriceSpikeVal, VolSpikeVal)
    wks0.update('C1', dicts[0]['currtime'])
    wks1.update('C2', dicts[-1]['prevtime'])
    if len(pricechangearray) > 900:
        print("Too many price symbols to print to sheet.  ", len(pricechangearray), "Pricespike flags, and ", len(volchangearray), " Volspike flags")
        avepricespike = sum(pricechangearray)/len(pricechangearray)
        print("Average Price Spike = ", avepricespike, ".  Current Threshold = ", PriceSpikeVal)
    elif len(volchangearray) > 900:
        print("Too many volume symbols to print to sheet.  ", len(pricechangearray), "Pricespike flags, and ", len(volchangearray), " Volspike flags")
        avevolspike = sum(volchangearray)/len(volchangearray)
        print("Average Volume Spike = ", avevolspike, ".  Current Threshold = ", VolSpikeVal)
    else:
        m = [pricechangearray, pricechangesymbolarray]
        n = [volchangearray, volchangesymbolarray]
        for row in m :
            rez1 = [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]
        for row in n :
            rez2 = [[n[j][i] for j in range(len(n))] for i in range(len(n[0]))]
        wks0.update("A3:B1000", rez1)
        wks0.update("D3:E1000", rez2)
        #wks.update('D2:D1500', [totalvolcheckarray])
        
def sheetarrays(PriceSpikeVal, VolSpikeVal):
    clearlists()
    for i in dicts:
        if i['delta%/time'] >= PriceSpikeVal:
            if type(i['delta%/time']) != float:
                print("Nonetype on ticker ", i['symbol'])
                return
            pricechangearray.append(i['delta%/time'])
            pricechangesymbolarray.append(i['symbol'])
        if i['volchange'] >= VolSpikeVal:
            if type(i['volchange']) != float:
                print("Nonetype on ticker ", i['symbol'])
                return
            volchangearray.append(i['volchange'])
            volchangesymbolarray.append(i['symbol'])
    #totalvolcheckarray.append(float(infodict['totalvolcheck']))

def dictionarys():
    for i in tickerlist:
        #currticker.config(text = i)
        #window.update()
        dictinitial['symbol'] = i
        dictcopy = dictinitial.copy()
        dictcopy['prevtime'] = time.time()
        dicts.append(dictcopy)
        

main()
