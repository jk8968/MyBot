import websocket, json, pprint, talib, numpy #talib is for indicators, websocket is for understanding binance data
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as dt
import pandas as pd
import config #file with API data
from binance.client import Client
from binance.enums import *
from pandas_datareader import data as pdr

buy = 0
sell = 0
profit = 0

in_position = False
cross = 0

from tvDatafeed import TvDatafeed, Interval

username = 'jk8968'
password = 'XQKiY5MgERK23wM'

tv=TvDatafeed(username=username,password=password)

df=tv.get_hist('BTCUSD','BINANCE',Interval.in_daily,n_bars=5000)
df = df.reset_index()

'''start = dt.datetime (2020, 1, 1)
end = dt.datetime (2021, 1, 1)
#now  = dt.datetime.now()
df = pdr.get_data_yahoo('BTC-USD', start, end)
#print (df)'''


for x in df.index:
    df['TP'] = (df['close'] + df['low'] + df['high'])/3
    df['MA200'] = df['TP'].rolling(200).mean()
    df['MA50'] = df['TP'].rolling(50).mean()

for i in df.index:
    #print(df.iloc[:,3][i])
    df['TP'] = (df['close'] + df['low'] + df['high'])/3
    df['std'] = df['TP'].rolling(20).std(ddof=0)
    df['MA'] = df['TP'].rolling(20).mean()
    df['BBUpper'] = df['MA'] + 2*df['std']
    df['BBLower'] = df['MA'] - 2*df['std']

    df['MA200'] = df['TP'].rolling(200).mean()
    df['MA50'] = df['TP'].rolling(50).mean()
    
    if (df["close"][i] > df["MA50"][i]).any() and in_position == True:

        if (df["close"][i] > df["BBUpper"][i]).any() and in_position == True:
            #take profit
            print("Sell at: ", df["close"][i])
            in_position = False
            sell = df["close"][i]
            profit = profit - df["close"][i]
            #print(sell)

        if (df["close"][i] < df["BBLower"][i]).any():
            print("Buy at: ", df["close"][i])
            in_position = True
            buy = df["close"][i]
            profit = profit + df["close"][i] #actual profit is first buy - this profit
            #print(in_position)

        if cross == -1 and in_position == True:
            a=0
            #sell

        if cross == 1 and in_position == False:
            a=1
            #buy 
    
    if (df["close"][i] > df['MA50'][i] and df["close"][i-1] < df['MA50'][i]):
        cross = 1
    if (df["close"][i] < df['MA50'][i] and df["close"][i-1] > df['MA50'][i]):
        cross = -1
    else:
        cross = 0

    #to zgornjo se razvi poglej kako deluje tale cross

    #to prej ni bilo noter sem dal iz drugega ko sem zdruzeval
    if (df["close"][i] > df["MA50"][i]).any() and in_position == False:
        if (df["close"][i] <= df["MA"][i]).any():
            in_position = True
            #position = 0
            print("Buy at: ", df["close"][i])
            #print("Date: ", modified["Date"][i])
            #plt.plot(df.iloc[:,0][i], df["Close"][i])
            #plt.plot(modified["Date"][i])
            buy = df["close"][i]
            profit = profit - df["close"][i]       
    
    if in_position == True and df["close"][i] <= 0.99*buy:
        print("Sell at: ", df["close"][i])
        in_position = False


close = df["close"]
upper = df["BBUpper"]
lower = df["BBLower"]
ma20 = df["MA"]
ma50 = df["MA50"]
plt.plot(close)
plt.plot(upper)
plt.plot(lower)
#plt.plot(ma20)
plt.plot(ma50)
plt.show()
print(profit)
print(df)

