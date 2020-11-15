##
## Query sample for  various Redis TimeSeries for querying stock prices
## and technical indicators
## Author: Prasanna Rajagopal
##
from redistimeseries.client import Client
from datetime import datetime
from iexfinance.stocks import get_historical_data
import pandas as pd

##
## Connect to Redis TimeSeries
##
rts = Client(host='127.0.0.1', port=6379)


##
## Query the Goldman Sachs range for RSI values
## 15-minute window
## "from_time = 0" indicates from the beginning
## "to_time = -1" indicates until the last value in the time series.
##
dailyRSI15MinRange = rts.range(  'DAILYRSI15MINRNG:GS'
                                , from_time = 0
                                , to_time = -1)
##dailyRSI15MinRange = rts.get('DAILYRSI15MINRNG:GS')
                                
print('****************GS RSI RANGE**************************************')
print(dailyRSI15MinRange)
print('****************GS RSI RANGE**************************************')

##
## Query the TimeSeries for Standard Deviation values for Goldman Sachs
## for each 15-minute window.
##
dailyGS15MinStdP = rts.range(  'INTRADAYPRICES15MINSTDP:GS'
                                , from_time = 0
                                , to_time = -1)
##dailyRSI15MinRange = rts.get('DAILYRSI15MINRNG:GS')
                                
print('****************GS STOCK PRICE STDP**************************************')
print(dailyGS15MinStdP)
print('****************GS STOCK PRICE STDP**************************************')

dailyGSPrice15MinRange = rts.range(  'INTRADAYPRICES15MINRNG:GS'
                                , from_time = 0
                                , to_time = -1)
##dailyRSI15MinRange = rts.get('DAILYRSI15MINRNG:GS')
                                
print('****************GOLDMAN SACHS PRICE RANGE************************')
print(dailyGSPrice15MinRange)
print('****************GOLDMAN SACHS PRICE RANGE**************************************')

dailyGSPrice15MinRange = rts.range(  'INTRADAYPRICES15MINRNG:GS'
                                , from_time = 0
                                , to_time = -1)
##dailyRSI15MinRange = rts.get('DAILYRSI15MINRNG:GS')
                                
print('****************GOLDMAN SACHS PRICE RANGE************************')
print(dailyGSPrice15MinRange)
print('****************GOLDMAN SACHS PRICE RANGE**************************************')

##
## Query each TimeSeries for a defined time range
## in this case it is from 1605260100 to 1605260940
##
dailyGSRSIValue = rts.range(  'DAILYRSI:GS'
                                , from_time = 1605260100
                                , to_time   = 1605260940)
##dailyRSI15MinRange = rts.get('DAILYRSI15MINRNG:GS')
                                
print('****************GOLDMAN SACHS RSI VALUE************************')
print(dailyGSRSIValue)
print('****************GOLDMAN SACHS RSI VALUE**************************************')

dailyGSPrice = rts.range(  'INTRADAYPRICES:GS'
                                , from_time = 1605260100
                                , to_time   = 1605260940)
##dailyRSI15MinRange = rts.get('INTRADAYPRICES:GS')
                                
print('****************GOLDMAN SACHS PRICES************************')
print(dailyGSPrice)
print('****************GOLDMAN SACHS PRICES************************')

allRSIValues = rts.mget(filters=['DESC=RELATIVE_STRENGTH_INDEX','TIMEFRAME=1_DAY'], with_labels=True)
##dailyRSI15MinRange = rts.get('DAILYRSI15MINRNG:GS')
                                
print('****************ALL RSI VALUE************************')
print(allRSIValues)
print('****************ALL RSI VALUE**************************************')


allStockPricesValues = rts.mget(filters=['DESC=SHARE_PRICE','PRICETYPE=INTRADAY'], with_labels=False)
##dailyRSI15MinRange = rts.get('DAILYRSI15MINRNG:GS')
                                
print('****************ALL STOCK PRICES************************')
print(allStockPricesValues)
print('****************ALL STOCK PRICES**************************************')

print('****************GOLDMAN SACHS PRICES DATES******************')

epoch = datetime(1970, 1, 1)
newdt2 = datetime.utcfromtimestamp(int(1605260100))
print('1605260100 - ' + str(newdt2.strftime('%Y-%m-%d %H:%M')))

#epoch = datetime(1970, 1, 1)
newdt2 = datetime.utcfromtimestamp(int(1605260940))
print('1605260940 - ' + str(newdt2.strftime('%Y-%m-%d %H:%M')))
print('****************GOLDMAN SACHS PRICES DATES************************')

print('****************GOLDMAN SACHS RSI VALUE DATES************************')
##
## Converting the dates from integer to string time format
##
epoch = datetime(1970, 1, 1)
newdt2 = datetime.utcfromtimestamp(int(1605260100))
print('1605260100 - ' + str(newdt2.strftime('%Y-%m-%d %H:%M')))

#epoch = datetime(1970, 1, 1)
newdt2 = datetime.utcfromtimestamp(int(1605260940))
print('1605260940 - ' + str(newdt2.strftime('%Y-%m-%d %H:%M')))

#epoch = datetime(1970, 1, 1)
newdt2 = datetime.utcfromtimestamp(int(1605260940))
print('1605260940 - ' + str(newdt2.strftime('%Y-%m-%d %H:%M')))

print('****************GOLDMAN SACHS RSI VALUE DATES************************')


#epoch = datetime(1970, 1, 1)
newdt2 = datetime.utcfromtimestamp(int(1605260820))
print('1605260820 - ' + str(newdt2.strftime('%Y-%m-%d %H:%M')))

newdt2 = datetime.utcfromtimestamp(int(1605261060))
print('1605261060 - ' + str(newdt2.strftime('%Y-%m-%d %H:%M')))
