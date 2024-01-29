import json, time, pandas as pd, talib
from tkinter import BOTH
import numpy
from tvDatafeed import TvDatafeed, Interval
import datetime
#from datetime import datetime

import config #file with API data
from binance.client import Client
from binance.enums import *

from threading import Thread
from websocket import create_connection, WebSocketConnectionClosedException

import votes as votes

from email_notifications import *
#-----------------------------------------------------------------------------------

RSI_PERIOD = 14
RSI_OVERSOLD = 20 #treshold
RSI_OVERBOUGHT = 85 #treshold

order_size = 50 

closes = []
daily_closes = []

data = {'Symbol': ['ADAUSDT', 'AVAXUSDT', 'ALGOUSDT', 'LUNAUSDT', 'LTCUSDT', 'SANDUSDT', 'BNBUSDT', 'MINAUSDT', 'THETAUSDT', 'HBARUSDT', 'XMRUSDT'],
        'Hourly_Closes': [[], [], [], [], [], [], [], [], [], [], []], 
        'Daily_Closes': [[], [], [], [], [], [], [], [], [], [], []], 
        'Hourly_50_MA':  [[], [], [], [], [], [], [], [], [], [], []], 
        'Hourly_200_MA':  [[], [], [], [], [], [], [], [], [], [], []], 
        'Daily_50_MA':  [[], [], [], [], [], [], [], [], [], [], []], 
        'RSI':  [[], [], [], [], [], [], [], [], [], [], []],
        'In_Position': [[False], [False], [False], [False], [False], [False], [False], [False], [False], [False], [False]],
        'Vote': [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]]}

df = pd.DataFrame(data)

number_of_rows = len(df.index)

username = 'jk8968'
password = 'XQKiY5MgERK23wM'
tv=TvDatafeed(username=username,password=password)

for i in range (number_of_rows):
    symbol = df['Symbol'][i]
    hourly_data=tv.get_hist(symbol,'BINANCE',Interval.in_1_hour,n_bars=200)
    closes_hourly = hourly_data['close'].to_numpy()
    df['Hourly_Closes'][i] = closes_hourly 

    daily_data=tv.get_hist(symbol,'BINANCE',Interval.in_daily,n_bars=50)
    closes_daily = daily_data['close'].to_numpy()
    df['Daily_Closes'][i] = closes_daily

    #vote = votes.vote(symbol = symbol)
    #df['Vote'][i] = vote

print(df)

#-----------------------------------------------------------------------------------
client = Client(config.API_KEY, config.API_SECRET, testnet=True)
#print(client.futures_account_balance())

def order(side, positionSide, quantity, symbol, order_type = ORDER_TYPE_MARKET):
    try:
        print("sending order")
        order = client.futures_create_order(symbol = symbol, side = side, positionSide =  positionSide,type = order_type, quantity = quantity, recvWindow = 120000, )
        print(order)
        return True     
    except Exception as e:
        return False
#-----------------------------------------------------------------------------------
def main():
    ws = None
    thread = None
    thread_running = True
    thread_keepalive = None

    def websocket_thread():
        global ws
        
        ws = create_connection("wss://stream.binance.com:9443/ws")
        ws.send(json.dumps({
                    "method": "SUBSCRIBE",
                    "params": ["adausdt@kline_1h", "avaxusdt@kline_1h", "algousdt@kline_1h", "lunausdt@kline_1h", "ltcusdt@kline_1h", "sandusdt@kline_1h", "bnbusdt@kline_1h", "minausdt@kline_1h", "thetausdt@kline_1h", "hbarusdt@kline_1h", "xrmusdt@kline_1h"], #"btcusdt@kline_1d"
                    #"params": ["adausdt@kline_5m", "avaxusdt@kline_5m", "algousdt@kline_5m", "lunausdt@kline_5m", "ltcusdt@kline_5m", "sandusdt@kline_5m", "bnbusdt@kline_5m", "minausdt@kline_5m", "thetausdt@kline_5m", "hbarusdt@kline_5m", "xrmusdt@kline_5m"], #"btcusdt@kline_1d"
                    "id": 1,}))

        thread_keepalive.start()
        while thread_running:
            try:
                data = ws.recv()
                if data != "":
                    msg = json.loads(data)
#-----------------------------------------------------------------------------------
                    ticker = msg['s']
                    #print(ticker)
                    candle = msg['k'] #looks up the kandle from the data stream
                    is_candle_closed =  candle ['x'] #is the candle closed 
                    close = candle ['c'] #closing price
                    #print(close)

                    if is_candle_closed == True:
                        print(ticker,'closed at: ', float(close))
                        for i in range (len(df.index)):
                            if df['Symbol'][i] == ticker:
                                
                                closes = numpy.array(df['Hourly_Closes'][i])
                                closes = numpy.append(closes, float(close))
                                closes = numpy.delete(closes, 0)
                                df['Hourly_Closes'][i] = closes
                                #df['Hourly_Closes'][i] += close
                                #print(df)

                                if (datetime.time(23,59,0) <= datetime.datetime.now().time() <= datetime.time(0,1,59)) :
                                    daily_data=tv.get_hist(ticker,'BINANCE',Interval.in_daily,n_bars=50)
                                    closes_daily = daily_data['close'].to_numpy()
                                    df['Daily_Closes'][i] = closes_daily
                                    #print('iiii')
                                
                                daily_closes = numpy.array(df['Daily_Closes'][i])

                                #-------------------------------------
                                #MA_12_EXP = talib.ema(closes, 12)
                                #MA_26_EXP = talib.ema(closes, 26)
                                
                                MACD = talib.MACD(closes, 12, 26)
                                current_MACD = MACD[-1]
                                df['MACD'][i] = current_MACD

                                MACD_9_EXP = talib.ema(MACD, 9)
                                current_MACD_9_EXP = MACD_9_EXP[-1]
                                df['Signal'][i] = current_MACD_9_EXP

                                MA_200 = talib.SMA(closes, 200)
                                last_MA_200 = MA_200[-1]
                                df['Hourly_200_MA'][i] = last_MA_200

                                in_position = df['In_position'][i]
                                quantity = closes[-1]/order_size

                                if (closes[-1] >= last_MA_200):
                                    if (current_MACD > current_MACD_9_EXP and in_position == False):
                                        order_succeeded = client.futures_create_order(symbol=ticker, side='BUY', positionSide = 'BOTH',type='MARKET', quantity=quantity)
                                        send_email(ticker, 'GO LONG', close)
                                        #order_succeeded = order(SIDE_BUY, QUANTITY, SYMBOL) #spot order
                                        if order_succeeded:
                                            in_position = True
                                            df['In_position'][i] = in_position
                                            print('buy order for: ', ticker, 'at: ', format(close))
                                    if (current_MACD < current_MACD_9_EXP and in_position == True):
                                        order_succeeded = client.futures_create_order(symbol= ticker, side='SELL', positionSide = 'BOTH',type='MARKET', quantity=quantity)
                                        send_email(ticker, 'SELL LONG', close)
                                        #order_succeeded = order(SIDE_SELL, QUANTITY, SYMBOL)
                                        if order_succeeded:
                                            in_position = False 
                                            df['In_position'][i] = in_position
                                            print('sell order for: ', ticker, 'at: ', format(close))
                                
                                if (closes[-1] < last_MA_200):
                                    if (current_MACD < current_MACD_9_EXP and df['In_Position'][i] == 'False'):
                                        order_succeeded = client.futures_create_order(symbol= ticker, side='SELL', positionSide = 'BOTH',type='MARKET', quantity=quantity)
                                        send_email(ticker, 'GO SHORT', close)
                                        #order_succeeded = order(SIDE_SELL, QUANTITY, SYMBOL)
                                        if order_succeeded:
                                            in_position = 'Short' 
                                            df['In_position'][i] = in_position
                                            print('sell order for: ', ticker, 'at: ', format(close))
                                    
                                    if (current_MACD > current_MACD_9_EXP and df['In_Position'][i] == 'Short'):
                                        order_succeeded = client.futures_create_order(symbol= ticker, side='BUY', positionSide = 'BOTH',type='MARKET', quantity=quantity)
                                        send_email(ticker, 'CLOSE SHORT', close)
                                        #order_succeeded = order(SIDE_SELL, QUANTITY, SYMBOL)
                                        if order_succeeded:
                                            in_position = 'False' 
                                            df['In_position'][i] = in_position
                                            print('sell order for: ', ticker, 'at: ', format(close))
                                    
                                #-------------------------------------
                                
                                # MA_50 = talib.SMA(closes, 50)
                                # last_MA_50 = MA_50[-1] #last MA50 calculated
                                # df['Hourly_50_MA'][i] = last_MA_50
                                # #print(df)

                                # MA_200 = talib.SMA(closes, 200)
                                # last_MA_200 = MA_200[-1]
                                # df['Hourly_200_MA'][i] = last_MA_200

                                # MA_50_daily = talib.SMA(daily_closes, 50)
                                # last_daily_MA_50 = MA_50_daily[-1] #last MA50 calculated
                                # df['Daily_50_MA'][i] = last_daily_MA_50
                                # #print(df)
                                
                                # rsi = talib.RSI(closes, RSI_PERIOD)
                                # last_rsi = rsi[-1]
                                # df['RSI'][i] = last_rsi
                                
                                # print('Daily_50_MA is: ', round(last_daily_MA_50, 3))
                                # print('Hourly_50_MA is: ', round(last_MA_50, 3))
                                # print('Hourly_200_MA is: ', round(last_MA_200, 3))
                                # print('The current RSI is: ', round(last_rsi, 3))
                                # bla = df['Vote'][i]
                                # print('The current vote is: ', bla)
                                # print('Time: ', datetime.datetime.now().time())
                                # print('-----------------')
                                # #print(df)

                                # in_position = df['In_position'][i]
                                # quantity = closes[-1]/order_size
                                # vote = df['Vote'][i]

                                # if(daily_closes[-1] > last_daily_MA_50):
                                #     if (closes[-1] > last_MA_200):
                                #         if (last_rsi < RSI_OVERSOLD) and in_position == False:
                                #             order_succeeded = client.futures_create_order(symbol=ticker, side='BUY', type='MARKET', quantity=quantity)
                                #             send_email(ticker, 'BUY', close)
                                #             #order_succeeded = order(SIDE_BUY, QUANTITY, SYMBOL) #spot order
                                #             if order_succeeded:
                                #                 in_position = True
                                #                 df['In_position'][i] = in_position
                                #                 print('buy order for: ', ticker, 'at: ', format(close), 'and RSI: ', format(last_rsi))
                                    
                                #         if (last_rsi > RSI_OVERSOLD):
                                #             vote = 0
                                #             df['Vote'][i] = vote
                                #             if in_position == True:
                                #                 order_succeeded = client.futures_create_order(symbol = ticker, side='SELL', type='MARKET', quantity=quantity)
                                #                 send_email(ticker, 'SELL', close)
                                #                 #order_succeeded = order(SIDE_SELL, QUANTITY, SYMBOL)
                                #                 if order_succeeded:
                                #                     in_position = False
                                #                     df['In_position'][i] = in_position
                                #                     print('sell order for: ', ticker, 'at: ', format(close), 'and RSI: ', format(last_rsi))
                                    
                                #     if (closes[-1] < last_MA_200):
                                #         if (last_rsi < RSI_OVERSOLD):
                                #             vote = vote + 1
                                #             df['Vote'][i] = vote
                                #             if vote == 3 and in_position == False:
                                #                 order_succeeded = client.futures_create_order(symbol=ticker, side='BUY', type='MARKET', quantity=quantity)
                                #                 send_email(ticker, 'BUY', close)
                                #                 #order_succeeded = order(SIDE_BUY, QUANTITY, SYMBOL)
                                #                 if order_succeeded:
                                #                     in_position = True 
                                #                     df['In_position'][i] = in_position
                                #                     print('buy order for: ', ticker, 'at: ', format(close), 'and RSI: ', format(last_rsi))
                                            
                                # if(daily_closes[-1] < last_daily_MA_50 and in_position == True):
                                #     order_succeeded = client.futures_create_order(symbol= ticker, side='SELL', type='MARKET', quantity=quantity)
                                #     send_email(ticker, 'SELL', close)
                                #     #order_succeeded = order(SIDE_SELL, QUANTITY, SYMBOL)
                                #     if order_succeeded:
                                #         in_position = False 
                                #         df['In_position'][i] = in_position
                                #         print('sell order for: ', ticker, 'at: ', format(close), 'and RSI: ', format(last_rsi))
 #-----------------------------------------------------------------------------------                               
                else:
                    msg = {}
            except ValueError as e:
                print(e)
                print("{} - data: {}".format(e, data))
            except Exception as e:
                print(e)
                print("{} - data: {}".format(e, data))
                #print(' ')
            # else:                             
            #     if "result" not in msg: #prints whole kline message
            #         #print(msg)

        try:
            if ws:
                ws.close()
        except WebSocketConnectionClosedException:
            pass
        finally:
            thread_keepalive.join()

    def websocket_keepalive(interval=30):
        global ws
        while ws.connected:
            ws.ping("keepalive")
            time.sleep(interval)

    thread = Thread(target=websocket_thread)
    thread_keepalive = Thread(target=websocket_keepalive)
    thread.start()


if __name__ == "__main__":
    main()

#--------------------------------------------------------------------------------------------------------------------------------

# import time
# import config
# from binance import ThreadedWebsocketManager

# api_key = '492d52be47e997636e68f2329316e5a89c671de94550027c599f586c1d49c7b5'
# api_secret = '1286ce921b36a7cb221d49849c6846b10dc72e713fae7ed4244b49d711c9b797'



# def main():

#     symbol = 'BNBBTC'

#     twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
#     # start is required to initialise its internal loop
#     twm.start()

#     def handle_socket_message(msg):
#         print(f"message type: {msg['e']}")
#         print(msg)

#     twm.start_kline_socket(callback=handle_socket_message, symbol=symbol)

#     # multiple sockets can be started
#     twm.start_depth_socket(callback=handle_socket_message, symbol=symbol)

#     # or a multiplex socket can be started like this
#     # see Binance docs for stream names
#     streams = ['bnbbtc@miniTicker', 'bnbbtc@bookTicker']
#     twm.start_multiplex_socket(callback=handle_socket_message, streams=streams)

#     twm.join()


# if __name__ == "__main__":
#    main()

#--------------------------------------------------------------------------------------------------------------------------------

# import asyncio
# import websockets


# async def candle_stick_data():
#     url = "wss://stream.binance.com:9443/ws/" #steam address
#     first_pair = 'bnbbtc@kline_1m' #first pair
#     async with websockets.connect(url+first_pair) as sock:
#         pairs = '{"method": "SUBSCRIBE", "params": ["xrpbtc@kline_1m","ethbtc@kline_1m" ],  "id": 1}' #other pairs

#         await sock.send(pairs)
#         print(f"> {pairs}")
#         while True:
#             resp = await sock.recv()
#             print(f"< {resp}")

# asyncio.get_event_loop().run_until_complete(candle_stick_data())

#--------------------------------------------------------------------------------------------------------------------------------

# from threading import Thread
# from binance.streams import ThreadedWebsocketManager
# import time

# listOfPairings=["ETHUSDT","BTCUSDT"]
# class Stream():
#     def start(self):
#         self.bm = ThreadedWebsocketManager()
#         self.bm.start()
#         self.stream_error = False
#         self.multiplex_list = list()

#         # listOfPairings: all pairs with USDT (over 250 items in list)
#         for pairing in listOfPairings:
#             self.multiplex_list.append(pairing.lower() + '@trade')
#         self.multiplex = self.bm.start_multiplex_socket(callback=self.realtime,streams=self.multiplex_list)

#         # monitoring the error
#         stop_trades = Thread(target=stream.restart_stream, daemon=True)
#         stop_trades.start()

#     def realtime(self, msg):
#         if 'data' in msg:
#             print(msg)
#         else:
#             self.stream_error = True

#     def restart_stream(self):
#         while True:
#             time.sleep(1)
#             if self.stream_error == True:
#                 self.bm.stop_socket(self.multiplex)
#                 time.sleep(5)
#                 self.stream_error = False
#                 self.multiplex = self.bm.start_multiplex_socket(callback=self.realtime, streams=self.multiplex_list)
# stream = Stream()
# stream.start()
# stream.bm.join()