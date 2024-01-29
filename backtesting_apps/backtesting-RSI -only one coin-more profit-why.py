import websocket, json, pprint, talib, numpy #talib is for indicators, websocket is for understanding binance data
import matplotlib.pyplot as plt

import yfinance as yf
import time
import datetime as dt
import pandas as pd

#import config #file with API data
from binance.client import Client
from binance.enums import *

from pandas_datareader import data as pdr

from tvDatafeed import TvDatafeed, Interval
import mplfinance as mpf

buy = 0
buy_price = 0
sell = 0
sell_price = 0
profit = 0

long = 0
short = 0

pivots = []
dates = []
counter = 0
lastPivot = 0

Range = [0,0,0,0,0,0,0,0,0,0]
dateRange = [0,0,0,0,0,0,0,0,0,0]

position = 0
in_position = False

#to comment select, ctl + K then ctrl + C
#to uncomment select, ctrl + K then ctrl + U

#Get Data yahoo
#---------------------------------------------------
start = dt.datetime (2020, 1, 1)
#end = dt.datetime (2022, 3, 29)
now  = dt.datetime.now()

df = yf.download('ADA-USD', start, now)
#df = pdr.get_data_yahoo('BTC-USD', start, now)
modified = df.reset_index()
#---------------------------------------------------

#Get Hourly Data
#---------------------------------------------------
username = 'jk8968'
password = 'XQKiY5MgERK23wM'

tv=TvDatafeed(username=username,password=password)

#btc_usd_data=tv.get_hist('GOOG','NASDAQ',Interval.in_1_hour,n_bars=10000)
btc_usd_data=tv.get_hist('ADAUSD','BINANCE',Interval.in_1_hour,n_bars=10000)
#btc_usd_data=tv.get_hist('BTCUSDT','BINANCE',Interval.in_1_hour,n_bars=10000)
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
    
for k in modified.index:
    modified['time'] = 1
    modified['TP'] = (modified['Close'] + modified['Low'] + modified['High'])/3
    modified['MA50'] = modified['TP'].rolling(50).mean()

modified['Date'] = pd.to_datetime(modified.Date)
modified['Date'] +=  pd.to_timedelta(modified.time, unit='h')
#modified['Date'] +=  30*pd.to_timedelta(modified.time, unit='min')

print(modified)
#---------------------------------------------------

#Checking if daily candle is above 50MA
#---------------------------------------------------
# a = 769

# for i in modified.index:
#     if i <= a:
#         start_date = modified['Date'][i]
#         end_date = modified['Date'][i+1]
#         after_start_date = modified_hourly["datetime"] >= start_date
#         before_end_date = modified_hourly["datetime"] < end_date
#         betwen_hours = after_start_date & before_end_date
#         #print(modified_hourly.loc[betwen_hours])
#         if (modified['Close'][i] > modified['MA50'][i]):
#             modified_hourly.loc[betwen_hours, 'MA_D'] = 1
#             #print(modified_hourly.loc[betwen_hours])
#         else:
#             modified_hourly.loc[betwen_hours, 'MA_D'] = 0
#---------------------------------------------------
number_of_rows = len(modified)
a = number_of_rows - 50
k = 0

    #b = modified['Date'][0]
    #print(datetime.date(b))
    #print(b.date())
    #print(modified_hourly['datetime'][0].date())
    
modified['try'] = 2

for i in modified.index:
    if (modified['Close'][i] > modified['MA50'][i]):
        modified['try'][i] = 1
    if (modified['Close'][i] < modified['MA50'][i]):
        modified['try'][i] = 0
    
modified_hourly['MA_D'] = 4
    #modified.is_copy = False
a = 0

    #print (modified['datetime'][0].date())
    #print(modified_hourly['datetime'][0].date())

for i in modified.index:
    if (modified['Date'][i].date() == modified_hourly['datetime'][a].date()):
            #print ('TRUE')
        while (modified_hourly['datetime'][a].date() == modified['Date'][i].date()):
                #c = modified['try'][i]
                #modified_hourly['MA_D'][a] = c
            modified_hourly['MA_D'][a] = modified['try'][i]
            if (a == len(modified_hourly) - 1):
                break
            else:
                a += 1

print(modified)

#Buying Strategy
#---------------------------------------------------
overbought = 72
oversold = 29
ledger = pd.DataFrame()
vote = 0
in_position = 'no'
profit = 0
buy = []
buydate = []
sell = []
selldate = []
rsi_buy = []
rsi_sell = []

for i in modified_hourly.index: 
   
    # if (modified_hourly['RSI'][i] < oversold) and  in_position == False:
    #     in_position = True
    #     #print('buy')
    #     #print(modified_hourly['close'][i])
    #     buy.append(modified_hourly['close'][i])
    #     buy_price = modified_hourly['close'][i]
    #     long = 1
    
    # if modified_hourly['close'][i] > 1.15 * buy_price and in_position == True and long == 1:
    #     in_position = False
    #     #print('buy')
    #     #print(modified_hourly['close'][i])
    #     sell.append(modified_hourly['close'][i])
    #     buy_price = 0
    #     long = 0
    
    # if modified_hourly['close'][i] < 0.98 * buy_price and in_position == True and long == 1:
    #     in_position = False
    #     #print('buy')
    #     #print(modified_hourly['close'][i])
    #     sell.append(modified_hourly['close'][i])
    #     buy_price = 0
    #     long = 0
    

    # if (modified_hourly['RSI'][i] > overbought) and  in_position == False:
    #     in_position = True
    #     #print('buy')
    #     #print(modified_hourly['close'][i])
    #     sell.append(modified_hourly['close'][i])
    #     sell_price = modified_hourly['close'][i]
    #     short = 1
    
    # if modified_hourly['close'][i] < 0.45 * sell_price and in_position == True and short == 1:
    #     in_position = False
    #     #print('buy')
    #     #print(modified_hourly['close'][i])
    #     buy.append(modified_hourly['close'][i])
    #     sell_price = 0
    #     short = 0
    
    # if modified_hourly['close'][i] > 1.03 * sell_price and in_position == True and short == 1:
    #     in_position = False
    #     #print('buy')
    #     #print(modified_hourly['close'][i])
    #     buy.append(modified_hourly['close'][i])
    #     sell_price = 0
    #     short = 0
  #---------------------------------------------------      
        
    # if (modified_hourly['MA_D'][i] == 1.0):
    #     if (modified_hourly['close'][i] >= modified_hourly['MA200'][i]): 
    #         if (modified_hourly['RSI'][i] < oversold) and  in_position == 'no':
    #             in_position = 'long'
    #             #print('buy')
    #             #print(modified_hourly['close'][i])
    #             buy.append(modified_hourly['close'][i])
    #             buydate.append(modified_hourly['datetime'][i])
    #             rsi_buy.append(modified_hourly['RSI'][i])
            
    #         if (modified_hourly['RSI'][i] > overbought):
    #             vote = 0
    #             if in_position == 'long':
    #                 in_position = 'no'
    #                 #print('sell')
    #                 #print(modified_hourly['close'][i])
    #                 sell.append(modified_hourly['close'][i])
    #                 selldate.append(modified_hourly['datetime'][i])
    #                 rsi_sell.append(modified_hourly['RSI'][i])


    #     if (modified_hourly['close'][i] < modified_hourly['MA200'][i]):
    #         if (modified_hourly['RSI'][i] < oversold) :
    #             vote = vote + 1
    #             if vote == 4 and in_position == 'no':
    #                 in_position = 'long'
    #                     #print('buy')
    #                     #print(modified_hourly['close'][i])
    #                 buy.append(modified_hourly['close'][i])
    #                 buydate.append(modified_hourly['datetime'][i])
    #                 rsi_buy.append(modified_hourly['RSI'][i])
    
    # if (modified_hourly['MA_D'][i] == 0 and in_position == 'long'):
    #          in_position = 'no'
    #          #print('sell')
    #          #print(modified_hourly['close'][i])
    #          sell.append(modified_hourly['close'][i])
    #          selldate.append(modified_hourly['datetime'][i])
    #          rsi_sell.append(1)

    if (modified_hourly['MA_D'][i] == 0):
        #if (modified_hourly['close'][i] <= modified_hourly['MA200'][i]): 
            if (modified_hourly['RSI'][i] < oversold) and  in_position == 'no':
                in_position = 'short'
                #print('buy')
                #print(modified_hourly['close'][i])
                sell.append(modified_hourly['close'][i])
                selldate.append(modified_hourly['datetime'][i])
                rsi_sell.append(modified_hourly['RSI'][i])
            
            if (modified_hourly['RSI'][i] > overbought):
                vote = 0
                if in_position == 'short':
                    in_position = 'no'
                    #print('sell')
                    #print(modified_hourly['close'][i])
                    buy.append(modified_hourly['close'][i])
                    buydate.append(modified_hourly['datetime'][i])
                    rsi_buy.append(modified_hourly['RSI'][i])

    if (modified_hourly['MA_D'][i] == 1 and in_position == 'short'):
             in_position = 'no'
             #print('sell')
             #print(modified_hourly['close'][i])
             buy.append(modified_hourly['close'][i])
             buydate.append(modified_hourly['datetime'][i])
             rsi_buy.append(1) 

    
    if (modified_hourly['MA_D'][i] == 1):
        #if (modified_hourly['close'][i] >= modified_hourly['MA200'][i]): 
            if (modified_hourly['RSI'][i] < oversold) and  in_position == 'no':
                in_position = 'long'
                #print('buy')
                #print(modified_hourly['close'][i])
                buy.append(modified_hourly['close'][i])
                buydate.append(modified_hourly['datetime'][i])
                rsi_buy.append(modified_hourly['RSI'][i])
            
            if (modified_hourly['RSI'][i] > overbought):
                vote = 0
                if in_position == 'long':
                    in_position = 'no'
                    #print('sell')
                    #print(modified_hourly['close'][i])
                    sell.append(modified_hourly['close'][i])
                    selldate.append(modified_hourly['datetime'][i])
                    rsi_sell.append(modified_hourly['RSI'][i])

    if (modified_hourly['MA_D'][i] == 0 and in_position == 'long'):
             in_position = 'no'
             #print('sell')
             #print(modified_hourly['close'][i])
             sell.append(modified_hourly['close'][i])
             selldate.append(modified_hourly['datetime'][i])
             rsi_sell.append(1)
    
                

#---------------------------------------------------
print(modified_hourly)

amount = 100

for b in range (0, len(buy)-1):
    print('buy', buy[b])
    print('buy date', buydate[b])
    print('rsi', rsi_buy[b])
    print(' ')
    print('sell', sell[b])
    print('sell date', selldate[b])
    print('rsi', rsi_sell[b])
    print(' ')
    profit = profit + sell[b] - buy[b]
    amount = (sell[b] * amount)/buy[b]
#print('profit', profit)
print('amount', amount)

#Plotting hourly
#---------------------------------------------------
close_h = modified_hourly["close"]
ma200_h = modified_hourly["MA200"]
date_h = modified_hourly["datetime"]
rsi_h = modified_hourly["RSI"]

ax1_h = plt.subplot(2,1,1)
ax1_h.plot(date_h,close_h,color='black')
ax1_h.grid(True)

plt.plot(date_h,ma200_h)

ax2_h = plt.subplot(2,1,2)
ax2_h.plot(date_h, rsi_h)
ax2_h.grid(True)
ax2_h.axhline(20, linestyle = '--', alpha = 0.5, color = '#ff0000')
ax2_h.axhline(85, linestyle = '--', alpha = 0.5, color = '#ff0000')

#mpf.plot(btc_usd_data.head(100),type='candle',style='yahoo',volume=True) #candle chart
plt.show()
#---------------------------------------------------

#print(modified)
#print(modified_hourly)

#for i in range (0, 4999):
    #print(modified_hourly['MA_D'][i])

# modified['Date'] = pd.to_datetime(modified.Date)
# modified['Date'] +=  pd.to_timedelta(modified.time, unit='h')
#print(modified)

# for i in range (4000, 5000):
#     print(modified_hourly['MA_D'][i])
#     if (modified_hourly['MA_D'][i] == 1.0):
#         print("iiii")
