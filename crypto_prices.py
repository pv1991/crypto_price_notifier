# Python Crypto Price Notifier Program
# Author: Peter Vuong
# Last Update: 30/09/2018

import json
import requests

# Retrieve ACX market buy price for a specific cryptocurrency.
def get_acx_prices(crypto):
    try:
        if (crypto == 'BTC'):
            r = requests.get('https://acx.io:443//api/v2/order_book.json?market=btcaud&asks_limit=1&bids_limit=1')

        elif (crypto == 'ETH'):
            r = requests.get('https://acx.io:443//api/v2/order_book.json?market=ethaud&asks_limit=1&bids_limit=1')

        elif (crypto == 'LTC'):
            r = requests.get('https://acx.io:443//api/v2/order_book.json?market=ltcaud&asks_limit=1&bids_limit=1')

        elif (crypto == 'BCH'):
            r = requests.get('https://acx.io:443//api/v2/order_book.json?market=bchaud&asks_limit=1&bids_limit=1')

        elif (crypto == 'XRP'):
            r = requests.get('https://acx.io:443//api/v2/order_book.json?market=xrpaud&asks_limit=1&bids_limit=1')
    
    except:
        print('ERROR: Unable to retrieve ACX ' + crypto + ' market buy price.')
        return 0
    
    else:
        try:
            response = r.json()
        
        except:
            buyPrice = float(-1)

        else:
            buyPrice = float(response['asks'][0]['price'])

        return buyPrice


# Retrieve BTC Markets market buy price for a specific cryptocurrency.
def get_btcmarkets_prices(crypto):
    try:
        if (crypto == 'BTC'):
            r = requests.get('https://api.btcmarkets.net/market/BTC/AUD/orderbook')

        elif (crypto == 'ETH'):
            r = requests.get('https://api.btcmarkets.net/market/ETH/AUD/orderbook')
            
        elif (crypto == 'LTC'):
            r = requests.get('https://api.btcmarkets.net/market/LTC/AUD/orderbook')  

        elif (crypto == 'BCH'):
            r = requests.get('https://api.btcmarkets.net/market/BCH/AUD/orderbook')

        elif (crypto == 'XRP'):
            r = requests.get('https://api.btcmarkets.net/market/XRP/AUD/orderbook')                 
    
    except:
        print('ERROR: Unable to retrieve BTC Markets ' + crypto + ' market buy price.')
        return 0
    
    else: 
        try:
            response = r.json()   
        except:
            buyPrice = float(-1)    

        else:
            buyPrice = float(response['asks'][0][0])

        return buyPrice   


# Retrieve Coinjar market buy price for a specific cryptocurrency.
def get_coinjar_prices(crypto):
    try:
        if (crypto == 'BTC'):
            r = requests.get('https://data.exchange.coinjar.com/products/BTCAUD/book?level=1')

        elif (crypto == 'ETH'):
            r = requests.get('https://data.exchange.coinjar.com/products/ETHAUD/book?level=1')
            
        elif (crypto == 'LTC'):
            r = requests.get('https://data.exchange.coinjar.com/products/LTCAUD/book?level=1')  

        elif (crypto == 'XRP'):
            r = requests.get('https://data.exchange.coinjar.com/products/XRPAUD/book?level=1')                 
    
    except:
        print('ERROR: Unable to retrieve Coinjar ' + crypto + ' market buy price.')
        return 0
    
    else: 
        if (crypto == 'BCH'):
            return 0
            
        else:
            try:
                response = r.json() 

            except:
                buyPrice = float(-1)  

            else:    
                buyPrice = float(response['asks'][0][0])

            return buyPrice
    

# Retrieve Coinspot market buy price for a specific cryptocurrency.
def get_coinspot_prices(crypto):
    try:
        r = requests.get('https://www.coinspot.com.au/pubapi/latest')     
    
    except:
        print('ERROR: Unable to retrieve Coinspot ' + crypto + ' market buy price.')
        return 0
    
    else: 
        try:
            response = r.json() 

        except:
            buyPrice = float(-1)      

        else:
            if (crypto == 'BTC'):
                buyPrice = float(response['prices']['btc']['ask'])

            elif (crypto == 'ETH'):
                buyPrice = float(response['prices']['eth']['ask'])

            elif (crypto == 'LTC'):
                buyPrice = float(response['prices']['ltc']['ask'])

            elif (crypto == 'BCH'):
                buyPrice = 0

            elif (crypto == 'XRP'):
                buyPrice = float(response['prices']['xrp']['ask'])

        return buyPrice
    
    
# Retrieve Huobi market buy price for a specific cryptocurrency.
def get_huobi_prices(crypto):
    try:
        if (crypto == 'BTC'):
            r = requests.get('https://api.huobi.com.au/market/depth?symbol=btcaud&type=step1')

        elif (crypto == 'ETH'):
            r = requests.get('https://api.huobi.com.au/market/depth?symbol=ethaud&type=step1')
            
        elif (crypto == 'LTC'):
            r = requests.get('https://api.huobi.com.au/market/depth?symbol=ltcaud&type=step1')  

        elif (crypto == 'BCH'):
            r = requests.get('https://api.huobi.com.au/market/depth?symbol=bchaud&type=step1')                 
    
    except:
        print('ERROR: Unable to retrieve Huobi ' + crypto + ' market buy price.')
        return 0
    
    else: 
        if (crypto == 'XRP'):
            return 0
            
        else:
            try:
                response = r.json()    

            except:
                buyPrice = float(-1)   
            
            else:
                buyPrice = float(response['tick']['asks'][0][0])

            return buyPrice
    

# Retrieve Independent Reserve market buy price for a specific cryptocurrency.
def get_independent_reserve_prices(crypto):
    try:
        if (crypto == 'BTC'):
            r = requests.get('https://api.independentreserve.com/Public/GetOrderBook?primaryCurrencyCode=xbt&secondaryCurrencyCode=aud')

        elif (crypto == 'ETH'):
            r = requests.get('https://api.independentreserve.com/Public/GetOrderBook?primaryCurrencyCode=eth&secondaryCurrencyCode=aud')
            
        elif (crypto == 'LTC'):
            r = requests.get('https://api.independentreserve.com/Public/GetOrderBook?primaryCurrencyCode=ltc&secondaryCurrencyCode=aud') 

        elif (crypto == 'BCH'):
            r = requests.get('https://api.independentreserve.com/Public/GetOrderBook?primaryCurrencyCode=bch&secondaryCurrencyCode=aud') 

        elif (crypto == 'XRP'):
            r = requests.get('https://api.independentreserve.com/Public/GetOrderBook?primaryCurrencyCode=xrp&secondaryCurrencyCode=aud')        
    
    except:
        print('ERROR: Unable to retrieve Independent Reserve ' + crypto + ' market buy price.')
        return 0
    
    else: 
        try:
            response = r.json()   

        except:
            buyPrice = float(-1)    
        
        else:
            buyPrice = float(response['SellOrders'][0]['Price'])
            
        return buyPrice


# Retrieve Bitfinex market buy/sell prices and volumes for a specific cryptocurrency.
def get_bitfinex_prices(crypto):
    try:
        if (crypto == 'BTC'):
            r = requests.get('https://api.bitfinex.com/v2/book/tBTCUSD/P0?len=1')

        elif (crypto == 'ETH'):
            r = requests.get('https://api.bitfinex.com/v2/book/tETHUSD/P0?len=1')
        
        elif (crypto == 'LTC'):
            r = requests.get('https://api.bitfinex.com/v2/book/tLTCUSD/P0?len=1')

        elif (crypto == 'BCH'):
            r = requests.get('https://api.bitfinex.com/v2/book/tBCHUSD/P0?len=1')

        elif (crypto == 'XRP'):
            r = requests.get('https://api.bitfinex.com/v2/book/tXRPUSD/P0?len=1')
    
    except:
        print('ERROR: Unable to retrieve Bitfinex ' + crypto + ' market buy price.')
        return 0
    
    else: 
        try:
            response = r.json()  

        except:
            buyPrice = float(-1) 

        else:    
            buyPrice = float(response[1][0])

        return buyPrice


# Retrieve Binance market buy/sell prices and volumes for a specific cryptocurrency.
def get_binance_prices(crypto):
    try:
        if (crypto == 'BTC'):
            r = requests.get('https://api.binance.com/api/v1/depth?symbol=BTCUSDT&limit=5')

        elif (crypto == 'ETH'):
            r = requests.get('https://api.binance.com/api/v1/depth?symbol=ETHUSDT&limit=5')
        
        elif (crypto == 'LTC'):
            r = requests.get('https://api.binance.com/api/v1/depth?symbol=LTCUSDT&limit=5')

        elif (crypto == 'BCH'):
            r = requests.get('https://api.binance.com/api/v1/depth?symbol=BCCUSDT&limit=5')

        elif (crypto == 'XRP'):
            r = requests.get('https://api.binance.com/api/v1/depth?symbol=XRPUSDT&limit=5')
    
    except:
        print('ERROR: Unable to retrieve Binance ' + crypto + ' market buy price.')
        return 0
    
    else: 
        try:
            response = r.json() 

        except:
            buyPrice = float(-1)  

        else:    
            buyPrice = float(response['asks'][0][0])

        return buyPrice