##
## Create various Redis TimeSeries for storing stock prices
## and technical indicators
## Author: Prasanna Rajagopal
##
from redistimeseries.client import Client
rts = Client(host='127.0.0.1', port=6379)

#
# TimeSeries for storing Relative Strength Indicator (RSI) for Goldman Sachs
# Symbol: GS
# Daily Values of RSI
#
rts.create('DAILYRSI:GS', labels={  'SYMBOL': 'GS'
                             , 'DESC':'RELATIVE_STRENGTH_INDEX'
                             , 'INDEX' :'DJIA'
                             , 'TIMEFRAME': '1_DAY'
                             , 'INDICATOR':'RSI'
                             , 'COMPANYNAME': 'GOLDMAN_SACHS_GROUP'})
#
# TimeSeries for storing Relative Strength Indicator (RSI) for Caterpillar
# Symbol: CAT
# Daily Values of RSI
#
rts.create('DAILYRSI:CAT', labels={  'SYMBOL': 'CAT'
                             , 'DESC':'RELATIVE_STRENGTH_INDEX'
                             , 'INDEX' :'DJIA'
                             , 'TIMEFRAME': '1_DAY'
                             , 'INDICATOR':'RSI'
                             , 'COMPANYNAME': 'CATERPILLAR'})

#
# TimeSeries for storing Range Aggregation for Relative Strength Indicator (RSI)
# for Goldman Sachs Group
# Range Aggregation will be applied on data from every 15-minute window
# Symbol: GS
# Daily Values of RSI
#
rts.create('DAILYRSI15MINRNG:GS', labels={  'SYMBOL': 'GS'
                                  , 'DESC':'RELATIVE_STRENGTH_INDEX'
                                  , 'INDEX' :'DJIA'
                                  , 'TIMEFRAME': '15_MINUTES'
                                  , 'AGGREGATION': 'RANGE'
                                  , 'INDICATOR':'RSI'
                                  , 'COMPANYNAME': 'GOLDMAN_SACHS_GROUP'})
#
# TimeSeries for storing last value for Relative Strength Indicator (RSI)
# for Goldman Sachs Group
# The "last" aggregation will be applied on data from every 15-minute window
# Symbol: GS
# Daily Values of RSI
#
rts.create('DAILYRSI15MINLAST:GS', labels={  'SYMBOL': 'GS'
                                  , 'DESC':'RELATIVE STRENGTH INDEX'
                                  , 'INDEX' :'DJIA'
                                  , 'TIMEFRAME': '15_MINUTES'
                                  , 'AGGREGATION': 'LAST'
                                  , 'INDICATOR':'RSI'
                                  , 'COMPANYNAME': 'GOLDMAN_SACHS_GROUP'})
#
# TimeSeries for storing first value for Relative Strength Indicator (RSI)
# for Goldman Sachs Group
# The "first" aggregation will be applied on data from every 15-minute window
# Symbol: GS
# Daily Values of RSI
#

rts.create('DAILYRSI15MINFIRST:GS', labels={  'SYMBOL': 'GS'
                                  , 'DESC':'RELATIVE STRENGTH INDEX'
                                  , 'INDEX' :'DJIA'
                                  , 'TIMEFRAME': '15_MINUTES'
                                  , 'AGGREGATION': 'FIRST'
                                  , 'INDICATOR':'RSI'
                                  , 'COMPANYNAME': 'GOLDMAN_SACHS_GROUP'})
#
# TimeSeries for storing minimum value for Relative Strength Indicator (RSI)
# for Goldman Sachs Group
# The "min" aggregation will be applied on data from every 15-minute window
# Symbol: GS
# Daily Values of RSI
#
rts.create('DAILYRSI15MINMIN:GS', labels={  'SYMBOL': 'GS'
                                  , 'DESC':'RELATIVE STRENGTH INDEX'
                                  , 'INDEX' :'DJIA'
                                  , 'TIMEFRAME': '15-MINUTES'
                                  , 'AGGREGATION': 'MIN'
                                  , 'INDICATOR':'RSI'
                                  , 'COMPANYNAME': 'GOLDMAN_SACHS_GROUP'})
#
# TimeSeries for storing maximum value for Relative Strength Indicator (RSI)
# for Goldman Sachs Group
# The "max" aggregation will be applied on data from every 15-minute window
# Symbol: GS
# Daily Values of RSI
#
rts.create('DAILYRSI15MINMAX:GS', labels={  'SYMBOL': 'GS'
                                  , 'DESC':'RELATIVE STRENGTH INDEX'
                                  , 'INDEX' :'DJIA'
                                  , 'TIMEFRAME': '15-MINUTES'
                                  , 'AGGREGATION': 'MAX'
                                  , 'INDICATOR':'RSI'
                                  , 'COMPANYNAME': 'GOLDMAN_SACHS_GROUP'})

#
# The "createrule" will apply the range, first, last, min, and max aggregations
# on the Goldman Sachs' daily RSI values and stores the aggregated value in
# the respective time series that we created above.
# You can do similar aggregations on other stocks in the market.
#
rts.createrule('DAILYRSI:GS', 'DAILYRSI15MINRNG:GS', 'range', 900*1000)
rts.createrule('DAILYRSI:GS', 'DAILYRSI15MINFIRST:GS', 'first', 900*1000)
rts.createrule('DAILYRSI:GS', 'DAILYRSI15MINLAST:GS', 'last', 900*1000)
rts.createrule('DAILYRSI:GS', 'DAILYRSI15MINMIN:GS', 'min', 900*1000)
rts.createrule('DAILYRSI:GS', 'DAILYRSI15MINMAX:GS', 'max', 900*1000)

#
# A Redis TimeSeries for storing the intraday prices
# for Goldman Sachs' stock price
#
#
rts.create('INTRADAYPRICES:GS', labels={ 'SYMBOL': 'GS'
                                       , 'DESC':'SHARE_PRICE'
                                       , 'INDEX' :'DJIA'
                                       , 'PRICETYPE':'INTRADAY'
                                       , 'COMPANYNAME': 'GOLDMAN_SACHS_GROUP'})

#
# We are creating various time series for storing the aggregations for
# Goldman Sachs' stock price.  
#
#
#
# Time series for storing range aggregation for GS
#
rts.create('INTRADAYPRICES15MINRNG:GS', labels={  'SYMBOL': 'GS'
                                       , 'DESC':'SHARE_PRICE'
                                       , 'INDEX' :'DJIA'
                                       , 'PRICETYPE':'RANGE'
                                       , 'AGGREGATION': 'RANGE'
                                       , 'DURATION':'15_MINUTES'
                                       , 'COMPANYNAME': 'GOLDMAN_SACHS_GROUP'})
#
# Time series for storing the minimum value for GS stock price
# within each 15 minute window. 
#
rts.create('INTRADAYPRICES15MINMIN:GS', labels={  'SYMBOL': 'GS'
                                       , 'DESC':'SHARE_PRICE'
                                       , 'INDEX' :'DJIA'
                                       , 'PRICETYPE':'MIN'
                                       , 'AGGREGATION': 'MIN'
                                       , 'DURATION':'15_MINUTES'
                                       , 'COMPANYNAME': 'GOLDMAN_SACHS_GROUP'})
#
# Time series for storing the maximum value for GS stock price
# within each 15 minute window. 
#
rts.create('INTRADAYPRICES15MINMAX:GS', labels={  'SYMBOL': 'GS'
                                       , 'DESC':'SHARE_PRICE'
                                       , 'INDEX' :'DJIA'
                                       , 'PRICETYPE':'MAX'
                                       , 'AGGREGATION': 'MAX'
                                       , 'DURATION':'15_MINUTES'
                                       , 'COMPANYNAME': 'GOLDMAN_SACHS_GROUP'})
#
# Time series for storing the standard deviation value for GS stock price
# within each 15 minute window. 
#
rts.create('INTRADAYPRICES15MINSTDP:GS', labels={  'SYMBOL': 'GS'
                                       , 'DESC':'SHARE_PRICE'
                                       , 'INDEX' :'DJIA'
                                       , 'PRICETYPE':'STDDEV'
                                       , 'AGGREGATION': 'STDDEV'
                                       , 'DURATION':'15_MINUTES'
                                       , 'COMPANYNAME': 'GOLDMAN_SACHS_GROUP'})

