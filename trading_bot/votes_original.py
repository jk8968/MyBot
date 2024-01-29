#from cmath import nan
#from symtable import Symbol
import websocket, json, pprint, talib, numpy #talib is for indicators, websocket is for understanding binance data
import matplotlib.pyplot as plt

import yfinance as yf
import time
import datetime  
import pandas as pd

#import config #file with API data
from binance.client import Client
from binance.enums import *

from pandas_datareader import data as pdr

from tvDatafeed import TvDatafeed, Interval
import mplfinance as mpf

from selenium import webdriver


buy = 0
buy_price = 0
sell = 0
sell_price = 0
profit = 0

position = 0
in_position = False


#to comment select, ctl + K then ctrl + C
#to uncomment select, ctrl + K then ctrl + U

#Get Hourly Data
#---------------------------------------------------
def vote(symbol):
    username = 'jk8968'
    password = 'XQKiY5MgERK23wM'

    #tv=TvDatafeed(auto_login=False)
    #webdriver.Chrome(executable_path="C:\Chrome_driver\chromedriver.exe")
    #tv=TvDatafeed(username=username,password=password, chromedriver_path='C:\Chrome_driver\chromedriver.exe')
    tv=TvDatafeed(username=username,password=password)

    df=tv.get_hist(symbol,'BINANCE',Interval.in_daily,n_bars=5000)
    modified = df.reset_index()

    btc_usd_data=tv.get_hist(symbol,'BINANCE',Interval.in_1_hour,n_bars=5000)
    modified_hourly = btc_usd_data.reset_index()

    #---------------------------------------------------

    #RSI hourly
    #---------------------------------------------------
    delta_hourly = modified_hourly['close'].diff(1)
    delta_hourly.dropna(inplace = True)
    
    positive_h = delta_hourly.copy()
    negative_h = delta_hourly.copy()

    positive_h[positive_h < 0] = 0
    negative_h[negative_h > 0] = 0

    days = 14

    average_gain_hourly = positive_h.rolling(window = days).mean()
    average_loss_hourly = abs(negative_h.rolling(window = days).mean())

    relative_strength_h = average_gain_hourly / average_loss_hourly
    RSI_h = 100.00 - (100.0 / (1.0 + relative_strength_h))
    #---------------------------------------------------

    #Moving Averages for hourly data
    #---------------------------------------------------
    for x in modified_hourly.index:
        #Moving Averages
        modified_hourly['TP'] = (modified_hourly['close'] + modified_hourly['low'] + modified_hourly['high'])/3
        modified_hourly['MA200'] = modified_hourly['TP'].rolling(200).mean()
        modified_hourly['MA50'] = modified_hourly['TP'].rolling(50).mean()
        modified_hourly["RSI"] = RSI_h
        modified_hourly['MA_D'] = 4
        
    for k in modified.index:
        modified['time'] = 1
        modified['TP'] = (modified['close'] + modified['low'] + modified['high'])/3
        modified['MA50'] = modified['TP'].rolling(50).mean()
        #modified['try'] = 0

    modified['datetime'] = pd.to_datetime(modified.datetime)
    modified['datetime'] -=  pd.to_timedelta(modified.time, unit='h')
    #---------------------------------------------------

    #Checking if daily candle is above 50MA
    #---------------------------------------------------
    number_of_rows = len(modified)
    a = number_of_rows - 50
    k = 0

    b = modified['datetime'][0]
    #print(datetime.date(b))
    #print(b.date())
    #print(modified_hourly['datetime'][0].date())
    
    modified['try'] = 2

    print(modified)
    for i in modified.index:
        if (modified['close'][i] > modified['MA50'][i]):
            modified['try'][i] = 1
        if (modified['close'][i] < modified['MA50'][i]):
            modified['try'][i] = 0
    
    #modified_hourly['MA_D'] = 4
    #modified.is_copy = False
    a = 0

    #print (modified['datetime'][0].date())
    #print(modified_hourly['datetime'][0].date())

    for i in modified.index:
        if (modified['datetime'][i].date() == modified_hourly['datetime'][a].date()):
            #print ('TRUE')
            while (modified_hourly['datetime'][a].date() == modified['datetime'][i].date()):
                #c = modified['try'][i]
                #modified_hourly['MA_D'][a] = c
                modified_hourly['MA_D'][a] = modified['try'][i]
                if (a == len(modified_hourly) - 1):
                    break
                else:
                    a += 1
        # if i <= a:
        #     # if (modified['close'][i] > modified['MA50'][i]):
        #     #     modified['try'] = 1
        #     # if (modified['close'][i] < modified['MA50'][i]):
        #     #       modified['try'] = 2
        #     # else:
        #     #      modified['try'] = 3
        #     ##print(k)
        #         start_date = modified['datetime'][i]
        #         if (i == a):
        #             end_date = modified['datetime'][i]
        #         else: 
        #             end_date = modified['datetime'][i+1]
        #         after_start_date = modified_hourly["datetime"] >= start_date
        #         before_end_date = modified_hourly["datetime"] < end_date
        #         betwen_hours = after_start_date & before_end_date
        #         #print(modified_hourly.loc[betwen_hours])
        #         if (modified['try'][i] == 1):
        #         #if (modified['close'][i] > modified['MA50'][i]):
        #             modified_hourly.loc[betwen_hours, 'MA_D'] = 1
        #             #print(modified_hourly.loc[betwen_hours])
        #         if (modified['try'][i] == 0):
        #         #if (modified['close'][i] < modified['MA50'][i]):
        #             modified_hourly.loc[betwen_hours, 'MA_D'] = 0
        #         #if (modified['close'][i] == modified['MA50'][i]):
        #             #modified_hourly.loc[betwen_hours, 'MA_D'] = 'x' 
    #---------------------------------------------------

    #Buying Strategy
    #---------------------------------------------------
    overbought = 72
    oversold = 29
    vote = 0
    b=0
    c=0
    d =0


    #for i in modified.index:
        #print(modified['try'][i])
        #print(modified['MA50'][i])
        #print(modified['close'][i])


    for i in range (0, 4999):
        #print(modified_hourly['MA_D'][i])
        if (modified_hourly['MA_D'][i] == 0):
            b = b + 1
        if (modified_hourly['MA_D'][i] == 1):
            c = c + 1
        #if (modified_hourly['MA_D'][i] == 'x'):
        if (modified_hourly['MA_D'][i] != 1 and modified_hourly['MA_D'][i] != 0):
            d = d + 1
    
    #print(b)
    #print(c)
    #print(d)

    vote  = 0
    j = 0

    for i in modified_hourly.index: 
        if (j == 0): 
            if (modified_hourly['MA_D'][i] == 1.0):
                if (modified_hourly['close'][i] < modified_hourly['MA200'][i]):
                    if (modified_hourly['RSI'][i] < oversold and modified_hourly['RSI'][i-1] > oversold):
                        vote = vote + 1
                        j = 1
                if (modified_hourly['close'][i] > modified_hourly['MA200'][i]):            
                    #if (modified_hourly['RSI'][i] > overbought):
                        vote = 0

            if (modified_hourly['MA_D'][i] == 0):
                vote = 0
        if (j != 0):
            j = j + 1
            if (j == 6):
                j = 0
            
    #print(modified)
    #print(modified_hourly)
    
#     #Plotting hourly
# #---------------------------------------------------
    
    print('vote:', vote)
    return(vote)


#---------------------------------------------------

#vote(symbol='AVAXUSDT')