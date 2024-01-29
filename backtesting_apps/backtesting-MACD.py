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

buy = []
sell = []
profit = 0

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
end = dt.datetime (2021, 1, 1)
now  = dt.datetime.now()

df = yf.download('BTC-USD', start, now)
modified = df.reset_index()
#---------------------------------------------------

#Get Hourly Data
#---------------------------------------------------
username = 'jk8968'
password = 'XQKiY5MgERK23wM'

tv=TvDatafeed(username=username,password=password)

btc_usd_data=tv.get_hist('BTCUSD','BINANCE',Interval.in_1_hour,n_bars=10000)
modified_hourly = btc_usd_data.reset_index()
#---------------------------------------------------

#ATR hourly
#---------------------------------------------------
# modified_hourly['H-L'] = modified_hourly['high'] - modified_hourly['low']
# modified_hourly['H-PC'] = abs(modified_hourly['high'] - modified_hourly['close'].shift(1))
# modified_hourly['L-PC'] = abs(modified_hourly['low'] - modified_hourly['close'].shift(1))

# modified_hourly['TR'] = modified_hourly[['H-L', 'H-PC', 'L-PC']].max(axis=1, skipna=False)
# modified_hourly['ATR'] = modified_hourly['TR'].rolling(14).mean()
#---------------------------------------------------

#MACD
#---------------------------------------------------
exp1 = modified_hourly['close'].ewm(span=12, adjust=False).mean()
exp2 = modified_hourly['close'].ewm(span=26, adjust=False).mean()

macd = exp1 - exp2
signal = macd.ewm(span=9,adjust=False).mean()
difference = macd - signal

#Moving Averages for hourly data
#---------------------------------------------------
for x in modified_hourly.index:
    #Moving Averages
    modified_hourly['TP'] = (modified_hourly['close'] + modified_hourly['low'] + modified_hourly['high'])/3
    modified_hourly['MA200'] = modified_hourly['TP'].rolling(200).mean()
    modified_hourly['MA100'] = modified_hourly['TP'].rolling(100).mean()
    modified_hourly['MA20'] = modified_hourly['TP'].rolling(20).mean()
    modified_hourly['MA50'] = modified_hourly['TP'].rolling(50).mean()
    #modified_hourly['RSI'] = 1
    modified_hourly['MACD'] = macd
    modified_hourly['Signal'] = signal
    modified_hourly['Histogram'] = difference


for k in modified.index:
    modified['time'] = 1
    modified['TP'] = (modified['Close'] + modified['Low'] + modified['High'])/3
    modified['MA50'] = modified['TP'].rolling(50).mean()

modified['Date'] = pd.to_datetime(modified.Date)
modified['Date'] +=  pd.to_timedelta(modified.time, unit='h')
#---------------------------------------------------

#Checking if daily candle is above 50MA
#---------------------------------------------------
a = 684

for i in modified.index:
    if i <= a:
        start_date = modified['Date'][i]
        end_date = modified['Date'][i+1]
        after_start_date = modified_hourly["datetime"] >= start_date
        before_end_date = modified_hourly["datetime"] < end_date
        betwen_hours = after_start_date & before_end_date
        #print(modified_hourly.loc[betwen_hours])
        if modified['Close'][i] > modified['MA50'][i]:
            modified_hourly.loc[betwen_hours, 'MA_D'] = 1
            #print(modified_hourly.loc[betwen_hours])
        else:
            modified_hourly.loc[betwen_hours, 'MA_D'] = 0
#---------------------------------------------------

#Buying Strategy
#---------------------------------------------------
cross = 0
touch = 0
count = 0
in_position = 0
buy_price = 0
sell_price = 0
atr_buy = 0
atr_short = 0

for i in modified_hourly.index: 

    if (modified_hourly['close'][i] >= modified_hourly['MA200'][i]):
        if (modified_hourly['MACD'][i] > modified_hourly['Signal'][i] and in_position == 0):
            in_position = 1
            buy_price = modified_hourly['close'][i]
            print('buy_price_', buy_price)
            buy.append(modified_hourly['close'][i])

        if (modified_hourly['MACD'][i] < modified_hourly['Signal'][i] and in_position == 1):
            in_position = 0
            sell_price = modified_hourly['close'][i]
            print('sell_price_', sell_price)
            sell.append(modified_hourly['close'][i])
   
#Shorting
#---------------------------------------------------
#shoer if you are below 200 ma    
''' if (modified_hourly['close'][i] < modified_hourly['MA200'][i]):
        if (modified_hourly['MACD'][i] < modified_hourly['Signal'][i] and in_position == 0):
            in_position = -1
            sell_price = modified_hourly['close'][i]
            print('short_sell_price_', sell_price)
            sell.append(modified_hourly['close'][i])
        
        if (modified_hourly['MACD'][i] > modified_hourly['Signal'][i] and in_position == -1):
            in_position = 0
            buy_price = modified_hourly['close'][i]
            print('buy_long_price_', buy_price)
            buy.append(modified_hourly['close'][i])'''
     

#---------------------------------------------------

amount = 100

for b in range (0, len(buy)-1):
    print('buy', buy[b])
    print('sell', sell[b])
    print(' ')
    profit = profit + sell[b] - buy[b]
    amount = (sell[b] * amount)/buy[b]

#print('profit', profit)
print('amount', amount)

#Plotting hourly
#---------------------------------------------------
close_h = modified_hourly["close"]
ma200_h = modified_hourly["MA200"]
ma50_h = modified_hourly["MA50"]
date_h = modified_hourly["datetime"]
# atr_h = modified_hourly["ATR"]

ax1_h = plt.subplot(2,1,1)
ax1_h.plot(date_h,close_h,color='black')
ax1_h.grid(True)

plt.plot(date_h,ma50_h)
plt.plot(date_h,ma200_h)

ax2_h = plt.subplot(2,1,2)
ax2_h.plot(date_h, signal)
ax2_h.plot(date_h, macd)
ax2_h.grid(True)
#ax2_h.axhline(20, linestyle = '--', alpha = 0.5, color = '#ff0000')
#ax2_h.axhline(85, linestyle = '--', alpha = 0.5, color = '#ff0000')

#mpf.plot(btc_usd_data.head(100),type='candle',style='yahoo',volume=True) #candle chart
plt.show()
#---------------------------------------------------

print(modified)
print(modified_hourly)
# modified['Date'] = pd.to_datetime(modified.Date)
# modified['Date'] +=  pd.to_timedelta(modified.time, unit='h')
#print(modified)

# for i in range (4000, 5000):
#     print(modified_hourly['MA_D'][i])
#     if (modified_hourly['MA_D'][i] == 1.0):
#         print("iiii")
