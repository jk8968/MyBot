#undervalued stocks
#price is what you pay. value is what you get

#magic Formula = Rank(Rank(Earnings Yield) + Rank(ROIC))
#Earnings Yield = EBIT/Enterprise Value -> bargain price -> EBIT - earnings before interest and taxes - levels the playing field for leverage 
#enterprise value -> value of the entire enterprise (everything, cash, options itd)
#ROIC = EBIT/(Net Fixed Assets + Net Working Capital) -> return on invested capital - focuses only on assets. excludes cash and interest bearing assets
#we rank stocks by both criterions -> sum them 

#exclude finance and insurance companies !!!

#invest in top 20-30 companies, accummulating 2-3 positions per month over 12 month period
#every month run the analysis, pick 2-3 stock and buy, repeat next month until portfolio is built
#rebalance every six months or 12 months

#ROIC = EBIT/(Total non-current assets + Current Assets - Current Liabilities)
#earnings yield = EBIT/EV

from get_financials_requests import *
from webscraping_yahoo_statistics import *

#-------------------------------------------------------------------
nasdaq100 = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'GOOG', 'TSLA', 'FB', 'NVDA', 'PYPL', 'ADBE', 'CMCSA', 'CSCO', 'INTC', 'PDD', 'NFLX', 'ASML', 'AMGN', 'ADP', 'AVGO', 'INTU', 'TXN', 'ISRG', 'MU', 'GILD', 'JD', 'COST', 'TMUS', 'REGN', 'ATVI', 'CSX', 'AMAT', 'ILMN', 'AMD', 'CTAS', 'ADI', 'MNST', 'DOCU', 'NTES', 'VRTX', 'EBAY', 'MCHP', 'PAYX', 'ROST', 'LRCX', 'MRNA', 'SPLK', 'CTXS', 'WDAY', 'KLAC', 'MXIM', 'BIDU', 'CTSH', 'MU', 'PEP', 'XEL', 'FAST', 'CTAS', 'BIDU', 'IDXX', 'EXC', 'PAYX', 'CSX', 'MRNA', 'SPLK', 'CTXS', 'WDAY', 'KLAC', 'MXIM', 'CTXS', 'CHKP', 'WBA', 'TXN', 'ASML', 'TCOM', 'CDW', 'LULU', 'PDD', 'ALGN', 'SWKS', 'WBA', 'EXC', 'EBAY', 'ZM', 'CDNS', 'CDW', 'TEAM', 'MELI', 'DLTR', 'VRSN', 'ALXN', 'PCAR', 'AVGO', 'KHC', 'BIDU', 'IDXX', 'MAR', 'NFLX', 'BIDU', 'SNPS', 'CERN', 'QCOM', 'ORLY']
dow = ['AAPL', 'AMGN', 'AXP', 'BA', 'CAT', 'CRM', 'CSCO', 'CVX', 'DIS', 'DOW', 'GS', 'HD', 'HON', 'IBM', 'INTC', 'JNJ', 'JPM', 'KO', 'MCD', 'MMM', 'MRK', 'MSFT', 'NKE', 'PG', 'TRV', 'UNH', 'V', 'VZ', 'WBA', 'WMT']
sp500 = [
    ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'GOOG', 'TSLA', 'FB', 'BRK.B', 'V', 'JPM', 'JNJ', 'NVDA', 'MA', 'PYPL', 'HD', 'DIS', 'BABA', 'CMCSA', 'NFLX', 'ADBE', 'INTC', 'VZ', 'CRM', 'ABT', 'CSCO', 'PEP', 'XOM', 'PFE', 'WMT', 'MRK', 'KO', 'T', 'ABBV', 'NKE', 'AVGO', 'PYPL', 'SBUX', 'BAC', 'TXN', 'COST', 'UNH', 'MDT', 'MCD', 'INTU', 'QCOM', 'CVX', 'HON', 'PM', 'WFC', 'DHR', 'NEE', 'LOW', 'GS', 'UPS', 'IBM', 'NOW', 'ISRG', 'AMGN', 'AMD', 'LIN', 'RTX', 'SBAC', 'INTC', 'FIS', 'CAT', 'FISV', 'SPGI', 'TMO', 'MU', 'GOOGL', 'GOOG', 'C', 'CHTR', 'VLO', 'MS', 'D', 'PYPL', 'DD', 'MSI', 'FDX', 'APD', 'BLK', 'BSX', 'ANTM', 'AXP', 'CI', 'GS', 'ITW', 'ZTS', 'HON', 'ADI', 'ADI', 'STZ', 'VFC', 'BKNG', 'SHW', 'MSFT', 'CCI', 'TMUS', 'MDLZ', 'IQV'],
    ['NOC', 'LMT', 'REGN', 'MU', 'IQV', 'KMB', 'ADI', 'ORCL', 'CI', 'ZTS', 'SPGI', 'HCA', 'EBAY', 'APD', 'EL', 'ANTM', 'CME', 'COP', 'FDX', 'ABB', 'ABMD', 'DHR', 'BDX', 'MCO', 'AMAT', 'COST', 'ES', 'CRM', 'DE', 'DG', 'ILMN', 'BMY', 'CTAS', 'GILD', 'PH', 'AVB', 'ANTM', 'QCOM', 'ALL', 'TJX', 'ETN', 'ICE', 'FIS', 'PAYX', 'BAX', 'SYY', 'PLD', 'PSX', 'GPN', 'BK', 'CMI', 'CDNS', 'STT', 'PSA', 'DLR', 'ECL', 'PSA', 'PSA', 'ADSK', 'RMD', 'RSG', 'ESS', 'BXP', 'CL', 'HUM', 'VRTX', 'ARE', 'EQR', 'SHW', 'CNC', 'RE', 'PAYC', 'IEX', 'VTR', 'MKC', 'DRE', 'MMC', 'PRU', 'FTV', 'WBA', 'EIX', 'BKR', 'CARR', 'VRSK', 'AMP', 'AJG', 'CMS', 'OXY', 'OKE', 'CERN', 'MLM', 'AKAM', 'AVY', 'BLL', 'ABT', 'NI', 'EOG', 'BKR', 'SWKS', 'XRAY', 'FTI', 'BR', 'GM'],
    ['DXC', 'EVRG', 'TSCO', 'TXT', 'JNPR', 'DVA', 'WRK', 'PKG', 'BIO', 'EXPE', 'SNPS', 'PVH', 'NRG', 'DISCK', 'SEE', 'DISH', 'UA', 'LEG', 'HBI', 'NWSA', 'RHI', 'COTY', 'PVH', 'HAS', 'WU', 'VFC', 'WDC', 'NCLH', 'CCL', 'SNA', 'FL', 'LKQ', 'LB', 'TRIP', 'KSS', 'OMC', 'CMA', 'RJF', 'DISCA', 'CPRI', 'GPS', 'FLS', 'ALB', 'DRI', 'KMX', 'IP', 'ADS', 'NWS', 'LB', 'PHM', 'F', 'KIM', 'PWR', 'AAL', 'LNC', 'MHK', 'VNO', 'HFC', 'CTL', 'MAC', 'JWN', 'UAA', 'MRO', 'AES', 'RRC', 'PRGO', 'APA', 'IVZ', 'OMC', 'AES', 'NOV', 'DVN', 'DISCK', 'DISH', 'XRX', 'DISCA', 'HRB', 'IVZ', 'NCLH', 'FOXA', 'KSS', 'NRG', 'UAA', 'SEE', 'MAC', 'VNO', 'DRI', 'HFC', 'MHK', 'F', 'AES', 'AAL', 'APA', 'RRC', 'CTL', 'LB', 'AES', 'IP', 'PHM', 'JWN', 'XRX'],
    ['NCLH', 'LNC', 'AES', 'IVZ', 'HRB', 'FOXA', 'NRG', 'DVN', 'UAA', 'MAC', 'SEE', 'VNO', 'MHK', 'XRX', 'HFC', 'DRI', 'APA', 'F', 'RRC', 'AAL', 'CTL', 'PHM', 'IP', 'JWN', 'AES', 'LB', 'CMA', 'ADS', 'GPS', 'FLS', 'CPRI', 'DISCA', 'CCL', 'KMX', 'PRGO', 'OMC', 'NWS', 'SNA', 'UAA', 'OMC', 'DISCK', 'KSS', 'LKQ', 'DISCA', 'PKG', 'TXT', 'JNPR', 'UA', 'WRK', 'PKG', 'DISCK', 'VFC', 'AAL', 'HBI', 'DVA', 'COTY', 'TXT', 'CCL', 'NCLH', 'LB', 'TRIP', 'KSS', 'OMC', 'CMA', 'RJF', 'ADS', 'NWS', 'LB', 'PHM', 'F', 'KIM', 'PWR', 'AAL', 'LNC', 'MHK', 'VNO', 'HFC', 'CTL', 'MAC', 'JWN', 'UAA', 'MRO', 'AES', 'RRC', 'PRGO', 'APA', 'IVZ', 'OMC', 'AES', 'NOV', 'DVN', 'DISCK', 'DISH', 'XRX', 'DISCA', 'HRB', 'IVZ', 'NCLH', 'FOXA', 'KSS', 'NRG', 'UAA', 'SEE', 'MAC', 'VNO', 'DRI', 'HFC', 'MHK', 'F', 'AES', 'AAL', 'APA', 'RRC', 'CTL', 'LB', 'AES', 'IP', 'PHM', 'JWN', 'XRX'],
    ['NOV', 'DVN', 'DISCK', 'DISH', 'XRX', 'DISCA', 'HRB', 'IVZ', 'NCLH', 'FOXA', 'KSS', 'NRG', 'UAA', 'SEE', 'MAC', 'VNO', 'DRI', 'HFC', 'MHK', 'F', 'AES', 'AAL', 'APA', 'RRC', 'CTL', 'LB', 'AES', 'IP', 'PHM', 'JWN', 'XRX', 'RJF', 'ADS', 'NWS', 'LB', 'PHM', 'F', 'KIM', 'PWR', 'AAL', 'LNC', 'MHK', 'VNO', 'HFC', 'CTL', 'MAC', 'JWN', 'UAA', 'MRO', 'AES', 'RRC', 'PRGO', 'APA', 'IVZ', 'OMC', 'AES', 'NOV', 'DVN', 'DISCK', 'DISH', 'XRX', 'DISCA', 'HRB', 'IVZ', 'NCLH', 'FOXA', 'KSS', 'NRG', 'UAA', 'SEE', 'MAC', 'VNO', 'DRI', 'HFC', 'MHK', 'F', 'AES', 'AAL', 'APA', 'RRC', 'CTL', 'LB', 'AES', 'IP', 'PHM', 'JWN', 'XRX', 'ADS', 'HRB', 'WU', 'HAS', 'KIM', 'VFC', 'LB', 'NWS', 'SNA', 'AAP', 'AME', 'GILD'],
    ['WBA', 'FDX', 'BSX', 'ADI', 'ALXN', 'NTRS', 'ULTA', 'MPC', 'RHI', 'FITB', 'PRU', 'KEY', 'ALB', 'OXY', 'FITB', 'PVH', 'WRK', 'XLNX', 'UHS', 'XLNX', 'XRAY', 'NTRS', 'O', 'XOM', 'NEM', 'KEYS', 'KMX', 'UDR', 'ALLE', 'PNW', 'DXCM', 'BF.B', 'JCI', 'STX', 'DXCM', 'EVRG', 'AJG', 'AMCR', 'CPB', 'LKQ', 'IDXX', 'KEYS', 'BF.B', 'ALXN', 'HES', 'HIG', 'PFG', 'KSU', 'MOS', 'JCI', 'LEN', 'CF', 'MOS', 'HSY', 'CERN', 'CF', 'NI', 'PNR', 'PKG', 'NEM', 'FMC', 'AIV', 'AAL', 'PWR', 'REG', 'XRAY', 'ESS', 'RE', 'RSG', 'EOG', 'AAL', 'VRSK', 'PNW', 'MLM', 'EQT', 'MAT', 'WRK', 'TRV', 'VRSK', 'APA', 'PBCT', 'PKI', 'ESS', 'APA', 'GLW', 'RSG', 'AIV', 'HIG', 'PBCT', 'STX', 'MAT', 'MPC', 'PFG', 'DXCM'],
    ['CF', 'NI', 'PNR', 'PKG', 'NEM', 'FMC', 'AIV', 'AAL', 'PWR', 'REG', 'XRAY', 'ESS', 'RE', 'RSG', 'EOG', 'AAL', 'VRSK', 'PNW', 'MLM', 'EQT', 'MAT', 'WRK', 'TRV', 'VRSK', 'APA', 'PBCT', 'PKI', 'ESS', 'APA', 'GLW', 'RSG', 'AIV', 'HIG', 'PBCT', 'STX', 'MAT', 'MPC', 'PFG', 'DXCM', 'EVRG', 'AJG', 'AMCR', 'CPB', 'LKQ', 'IDXX', 'KEYS', 'BF.B', 'ALXN', 'HES', 'HIG', 'PFG', 'KSU', 'MOS', 'JCI', 'LEN', 'CF', 'MOS', 'HSY', 'CERN', 'CF', 'NI', 'PNR', 'PKG', 'NEM', 'FMC', 'AIV', 'AAL', 'PWR', 'REG', 'XRAY', 'ESS', 'RE', 'RSG', 'EOG', 'AAL', 'VRSK', 'PNW', 'MLM', 'EQT', 'MAT', 'WRK', 'TRV', 'VRSK', 'APA', 'PBCT', 'PKI', 'ESS', 'APA', 'GLW', 'RSG', 'AIV', 'HIG', 'PBCT', 'STX', 'MAT', 'MPC', 'PFG', 'DXCM', 'APA', 'PBCT', 'RSG', 'AES', 'HIG', 'XRAY'],
    ['AAL', 'VRSK', 'PNW', 'MLM', 'EQT', 'MAT', 'WRK', 'TRV', 'VRSK', 'APA', 'PBCT', 'PKI', 'ESS', 'APA', 'GLW', 'RSG', 'AIV', 'HIG', 'PBCT', 'STX', 'MAT', 'MPC', 'PFG', 'DXCM', 'APA', 'PBCT', 'RSG', 'AES', 'HIG', 'XRAY', 'KMX', 'FDX', 'BSX', 'ADI', 'ALXN', 'NTRS', 'ULTA', 'MPC', 'RHI', 'FITB', 'PRU', 'KEY', 'ALB', 'OXY', 'FITB', 'PVH', 'WRK', 'XLNX', 'UHS', 'XLNX', 'XRAY', 'NTRS', 'O', 'XOM', 'NEM', 'KEYS', 'KMX', 'UDR', 'ALLE', 'PNW', 'DXCM', 'BF.B', 'JCI', 'STX', 'DXCM', 'EVRG', 'AJG', 'AMCR', 'CPB', 'LKQ', 'IDXX', 'KEYS', 'BF.B', 'ALXN', 'HES', 'HIG', 'PFG', 'KSU', 'MOS', 'JCI', 'LEN', 'CF', 'MOS', 'HSY', 'CERN', 'CF', 'NI', 'PNR', 'PKG', 'NEM', 'FMC', 'AIV', 'AAL', 'PWR', 'REG', 'XRAY', 'ESS', 'RE', 'RSG', 'EOG', 'AAL', 'VRSK', 'PNW', 'MLM', 'EQT', 'MAT', 'WRK', 'TRV', 'VRSK', 'APA', 'PBCT', 'PKI', 'ESS', 'APA', 'GLW', 'RSG', 'AIV', 'HIG', 'PBCT', 'STX', 'MAT', 'MPC', 'PFG', 'DXCM', 'EVRG', 'AJG', 'AMCR', 'CPB', 'LKQ', 'IDXX', 'KEYS', 'BF.B', 'ALXN', 'HES', 'HIG', 'PFG', 'KSU', 'MOS', 'JCI', 'LEN', 'CF', 'MOS', 'HSY', 'CERN', 'CF', 'NI', 'PNR', 'PKG', 'NEM', 'FMC', 'AIV', 'AAL', 'PWR', 'REG', 'XRAY', 'ESS', 'RE', 'RSG', 'EOG', 'AAL', 'VRSK', 'PNW', 'MLM', 'EQT', 'MAT', 'WRK', 'TRV', 'VRSK', 'APA', 'PBCT', 'PKI', 'ESS', 'APA', 'GLW', 'RSG', 'AIV', 'HIG', 'PBCT', 'STX', 'MAT', 'MPC', 'PFG', 'DXCM', 'APA', 'PBCT', 'RSG', 'AES', 'HIG', 'XRAY']
]
#-------------------------------------------------------------------
#tickers = ['AAPL','GOOG','MSFT', 'META', 'XOM', 'JNJ', 'AMZN' , 'MA', 'CVX', 'ADBE', 'PEP', 'MCD', 'PHG', 'NVDA'] #working
tickers = ['AAPL','GOOG']
#tickers = nasdaq100 #ne dela se
#tickers = dow #tudi ne dela
#-------------------------------------------------------------------
#get data
print('getting data baby')
print('')
financials = get_financials(tickers)
print(financials)
print('')
print('geting statistics')
statistics = get_data(tickers)
print(statistics)
print(' ')
#-------------------------------------------------------------------
#magic formula
list = []
for ticker in tickers:
    row = []
    #print(ticker)
    EBIT = str_to_int((financials.loc[(financials['Ticker'] == ticker) & (financials['Type'] == 'annualEBIT')][datetime.date.today().year]).to_string())
    #print(EBIT)
    Total_Non_Cur_Assets = str_to_int((financials.loc[(financials['Ticker'] == ticker) & (financials['Type'] == 'annualTotalNonCurrentAssets')][datetime.date.today().year]).to_string())
    #print(Total_Non_Cur_Assets)
    Cur_Assets =  str_to_int((financials.loc[(financials['Ticker'] == ticker) & (financials['Type'] == 'annualCurrentAssets')][datetime.date.today().year]).to_string())
    #print(Cur_Assets)
    Cur_Liabilities = str_to_int((financials.loc[(financials['Ticker'] == ticker) & (financials['Type'] == 'annualCurrentLiabilities')][datetime.date.today().year]).to_string())
    #print(Cur_Liabilities)

    ROIC = EBIT/(Total_Non_Cur_Assets + Cur_Assets - Cur_Liabilities)
    #print(ROIC)
    row.append(ticker)
    row.append(ROIC)
    #list.append(row)
    #df = pd.DataFrame(list)

    enterprise_value = str_to_int((statistics.loc[statistics['Ticker']==ticker]['Enterprise Value']).to_string())
    #print(enterprise_value)
    earnings_yield = EBIT/enterprise_value
    row.append(earnings_yield)
    #print(earnings_yield)
    list.append(row)
    df = pd.DataFrame(list, columns=('Ticker', 'ROIC', 'Earning Yield'))
#-------------------------------------------------------------------
#valuation
list = []
discount_rate = 0.15
terminal_value = 10
values = []
values1 =  []
values2 = []
grow_rates = []
for ticker in tickers:
    row = []
    #print(ticker)
    free_cash_flow = str_to_int((financials.loc[(financials['Ticker'] == ticker) & (financials['Type'] == 'annualFreeCashFlow')][datetime.date.today().year]).to_string())
    #print(free_cash_flow)
    growth_rate_future_estimate = str_to_int((statistics.loc[statistics['Ticker']==ticker]['Next 5 Years (per annum)']).to_string())
    growth_rate_past = str_to_int((statistics.loc[statistics['Ticker']==ticker]['Past 5 Years (per annum)']).to_string())
    growth_rate_median = (growth_rate_future_estimate + growth_rate_past)/2
    growth_rates=[growth_rate_future_estimate, growth_rate_past, growth_rate_median]
    #print(growth_rates)
    shares_outstanding = str_to_int((statistics.loc[statistics['Ticker']==ticker]['Shares Outstanding']).to_string())
    #print(shares_outstanding)
    cash = str_to_int((statistics.loc[statistics['Ticker']==ticker]['Total Cash']).to_string())
    #print(cash)
    total_debt = str_to_int((statistics.loc[statistics['Ticker']==ticker]['Total Debt']).to_string())
    #print(total_debt)
    currency = (financials.loc[(financials['Ticker'] == ticker) & (financials['Type'] == 'annualFreeCashFlow')]['Currency']).to_string()
    #print(currency)1b

    i = 0
    valuation = 0
    t=0

    for g in growth_rates:
        while (i<=10):
            valuation = valuation + free_cash_flow*((1+g)**i)/((1+discount_rate)**i)
            free_cash_flow_year_10 = free_cash_flow*((1+g)**i)
            i = i+1
        t=t+1
        free_cash_flow_year_10 = free_cash_flow_year_10 * terminal_value
        discounted_cash_flow_year_10 = free_cash_flow_year_10/((1+discount_rate)**10) 

        valuation = (valuation + discounted_cash_flow_year_10)/shares_outstanding
        
        if t == 1:
            values.append(valuation)
        if t == 2:
            values1.append(valuation)
        if t == 3:
            values2.append(valuation)

        valuation = 0
        i=0
        #print(valuation)
        #print(ticker, valuation, currency)

df['Valuation_g1'] = values
df['Valuation_g2'] = values1
df['Valuation_g_med'] = values2

#-------------------------------------------------------------------

df['CombinedRank'] = df['ROIC'].rank(ascending=False,na_option='bottom') + df['Earning Yield'].rank(ascending=False,na_option='bottom')
df['Rank'] = df['CombinedRank'].rank(method='first')

df = df.sort_values('Rank', ascending=True)

print(df)

#print(df['Next 5 Years (per annum)']['CVX'])

#dodaj se cene

import customtkinter
from tkinter import *
from CTkTable import *
from tkinter import ttk

customtkinter.set_appearance_mode('dark') #colour
customtkinter.set_default_color_theme('green') #for buttons

app = customtkinter.CTk() #root element
#app.title('Title')
app.geometry ('350x350')

frame = customtkinter.CTkFrame(master=app)
frame.pack(pady = 20, padx = 30, fill='both', expand = True)

button = customtkinter.CTkButton(master=frame, text = 'Run Programm', command = '') #button with code function
button.pack(pady = 12, padx = 10)

tree = ttk.Treeview(frame, column=("Ticker", "Type", "2023", 'Val_g1', 'Val_g2','Val_gM','CombRank','Rank_Magic_F'), show='headings', height=5)
tree.column("# 1", anchor=CENTER)
tree.heading("# 1", text="Ticker")
tree.column("# 2", anchor=CENTER)
tree.heading("# 2", text="ROIC")
tree.column("# 3", anchor=CENTER)
tree.heading("# 3", text="earnings_yield")
tree.column("# 4", anchor=CENTER)
tree.heading("# 4", text="Valuation_g1")
tree.column("# 5", anchor=CENTER)
tree.heading("# 5", text="Valuation_g2")
tree.column("# 6", anchor=CENTER)
tree.heading("# 6", text="Valuation_g_mid")
tree.column("# 7", anchor=CENTER)
tree.heading("# 7", text="Combined_Rank")
tree.column("# 8", anchor=CENTER)
tree.heading("# 8", text="Rank_Magic_F")
tree.pack(pady = 10, padx = 10)

a = [['Ticker','ROIC','Earnings_Yield','Valuation_g1','Valuation_g2','Valuation_g_mid','CombinedRank','Rank']]
table = CTkTable(master=frame, values=a)
for ind in df.index: 
    tree.insert('', 'end', text="1", values=df.loc[ind, :].values.tolist())
    a.append(df.loc[ind, :].values.tolist())

table = CTkTable(master=frame, values=a)
table.pack(expand=True, fill="both", padx=20, pady=20)
    
    #print(financials.iloc[i])
app.mainloop()
