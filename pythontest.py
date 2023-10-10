import numpy as np
import csv
import robin_stocks
import time
import datetime
import pandas as pd

closingdata = []
s12 = 2/(12+1)
s26 = 2/(26+1)
s9 = 2/(9+1)
EMAprev12 = []
EMAprev26 = []

def main():  
    #this pulls historicals for the past month.  
    robin_stocks.robinhood.authentication.login('wadepe@yahoo.com', 'Robinhood1!')
    #data = robin_stocks.robinhood.stocks.get_stock_historicals('GME', interval='day',span='3month')
    #print(data)
    #print(data[1]['close_price'])    indexing into an array of dicts

    data = robin_stocks.robinhood.stocks.get_stock_historicals('SPY', interval='day', span='year')
    for i in data:
        closingdata.append(float(i['close_price']))
    EMAy12 = data.ewm(span=12, adjust=False, min_periods=12).mean()
    EMAy26 = data.ewm(span=26, adjust=False, min_periods=26).mean()

    #data26 = closingdata[-26:]
    #data12 = closingdata[-12:]
    #EMAprev26.append(data26[0])
    #print(data26)
    #for j in range(len(data26)):
    #    if j != 0:
    #        if j > 12:
    #            print(data26[int(j)]*s26 + EMAprev26[int(j - 1)] - EMAprev26[int(j - 1)] * s26)
    #        EMAprev26.append(data26[int(j)]*s26 + EMAprev26[int(j - 1)] - EMAprev26[int(j - 1)] * s26)
    #EMAprev12.append(data12[0])
    #for j in range(len(data12)):
    #    if j != 0:
    #        print("         ", data12[int(j)]*s12 + EMAprev12[int(j - 1)] - EMAprev12[int(j - 1)] * s12)
    #        EMAprev12.append(data12[int(j)]*s12 + EMAprev12[int(j - 1)] - EMAprev12[int(j - 1)] * s12)
    #EMAy12 = EMAprev12[-1]
    #print(EMAy12)
    #EMAy26 = EMAprev26[-1]
    #print(EMAy26)
    #EMAy9 = 


    while(True):
        hold = robin_stocks.robinhood.stocks.get_latest_price('SPY')
        price = float(hold[0])
        EMA12 = price*s12 + EMAy12 - EMAy12 * s12
        EMA26 = price*s26 + EMAy26 - EMAy26 * s26
        print(EMA12-EMA26, " : ", EMA12," : ", EMA26)
        # EMA9 = (price * (s9/(1+9))) + EMAy9(1-(s9/(1+9)))
        time.sleep(10)

main()
