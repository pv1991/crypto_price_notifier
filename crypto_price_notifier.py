# Python Crypto Price Notifier Program
# Author: Peter Vuong
# Last Update: 30/09/2018
#
# Usage: python crypto_price_notifier.py

import configparser
import datetime
from forex_python.converter import CurrencyRates
import json
import pprint
import telegram
from time import sleep

from crypto_prices import get_acx_prices
from crypto_prices import get_btcmarkets_prices
from crypto_prices import get_coinjar_prices
from crypto_prices import get_coinspot_prices
from crypto_prices import get_huobi_prices
from crypto_prices import get_independent_reserve_prices
from crypto_prices import get_bitfinex_prices
from crypto_prices import get_binance_prices

exchangeFees = {
                'acx' : 0.002,
                'btcmarkets' : 0.0085,
                'coinjar' : 0.005,
                'coinspot' : 0.001,
                'huobi' : 0.002,
                'independentreserve' : 0.005,
                'bitfinex' : 0.002,
                'binance' : 0.001
                }

TELEGRAM_USERS = ''

# Gather market buy prices from the different exchanges for a specific cryptocurrency.
def get_crypto_prices(crypto):
    cryptoPrices = {
                    'acx' : get_acx_prices(crypto),
                    'btcmarkets' : get_btcmarkets_prices(crypto),
                    'coinjar' : get_coinjar_prices(crypto),
                    'coinspot' : get_coinspot_prices(crypto),
                    'huobi' : get_huobi_prices(crypto), 
                    'independentreserve' : get_independent_reserve_prices(crypto),
                    'bitfinex' : get_bitfinex_prices(crypto),
                    'binance' : get_binance_prices(crypto)
                    }

    return cryptoPrices


# Calcualte average buy price for a specific cryptocurrency.
def calculate_avg_buy_price(crypto):
    buyPrices = get_crypto_prices(crypto)
    adjustedBuyPrices = buyPrices.copy()

    # Factor in exchange fees into exchange buy prices and convert USD to AUD.
    for item in buyPrices:
        adjustedBuyPrices[item] = buyPrices[item] * (1 + exchangeFees[item])

    totalPriceAUD = 0
    totalPriceUSD = 0
    countAUD = 0
    countUSD = 0
    for buyKey in buyPrices:
        adjustedBuyPrice = adjustedBuyPrices[buyKey]
        if (adjustedBuyPrice > 0):
            if (buyKey in ('bitfinex', 'binance')):
                totalPriceUSD += adjustedBuyPrice
                countUSD = countUSD + 1

            else:
                totalPriceAUD += adjustedBuyPrice
                countAUD = countAUD + 1
                
    avgBuyPriceAUD = totalPriceAUD / countAUD
    avgBuyPriceUSD = totalPriceUSD / countUSD
    
    return (avgBuyPriceAUD, avgBuyPriceUSD)


# Display all the buy prices currently available for all cryptocurrencies.
def display_crypto_prices(telegramFlag, bot, chatId):
    dateTime = str(datetime.datetime.now()).split('.')[0]
    c = CurrencyRates()
    exchangeRate = c.get_rate('USD', 'AUD')

    print(dateTime)
    print('')
    message = '*---- ' + dateTime + ' ----*'
    send_to_telegram(bot, chatId, message)

    cryptoList = ['BTC', 'ETH', 'LTC', 'BCH', 'XRP']
    for crypto in cryptoList:
        avgBuyPrices = calculate_avg_buy_price(crypto)
        buyPrices = get_crypto_prices(crypto)
        telegramMsgs = []
        
        print(crypto + ' PRICES:')
        message = '*' + crypto + ' PRICES:*'
        telegramMsgs.append(message)
        for buyKey in buyPrices:
            if (buyKey in ('bitfinex', 'binance')):
                convertedBuyPrice = buyPrices[buyKey] * exchangeRate
                priceInfo = buyKey + ': ' + str(round(buyPrices[buyKey], 4)) + ' USD (' + str(round(convertedBuyPrice, 4)) + ' AUD)'
                message = buyKey + ': *$' + str(round(buyPrices[buyKey], 2)) + ' USD ($' + str(round(convertedBuyPrice, 2)) + ' AUD)*'
            
            else:
                priceInfo = buyKey + ': ' + str(round(buyPrices[buyKey], 4)) + ' AUD'
                message = buyKey + ': *$' + str(round(buyPrices[buyKey], 2)) + ' AUD*'

            print(priceInfo)
            telegramMsgs.append(message)

        print('')
        telegramMsgs.append('')
        if (previousAvgBuyPriceAUD[crypto] > 0):
            currentAvgBuyPriceAUD = avgBuyPrices[0]
            avgPercentageChangeAUD = ((currentAvgBuyPriceAUD / previousAvgBuyPriceAUD[crypto]) - 1) * 100
            previousAvgBuyPriceAUD[crypto] = currentAvgBuyPriceAUD

            print('Average % Change (AUD): ' + str(round(avgPercentageChangeAUD, 2)))
            message = 'Average Change AUD: *' + str(round(avgPercentageChangeAUD, 2)) + '%*'
            telegramMsgs.append(message)

        else:
            currentAvgBuyPriceAUD = avgBuyPrices[0]
            previousAvgBuyPriceAUD[crypto] = currentAvgBuyPriceAUD
            avgPercentageChangeAUD = 0

        if (previousAvgBuyPriceUSD[crypto] > 0):
            currentAvgBuyPriceUSD = avgBuyPrices[1]
            avgPercentageChangeUSD = ((currentAvgBuyPriceUSD / previousAvgBuyPriceUSD[crypto]) - 1) * 100
            previousAvgBuyPriceUSD[crypto] = currentAvgBuyPriceUSD

            print('Average % Change (USD): ' + str(round(avgPercentageChangeUSD, 2)))
            message = 'Average Change USD: *' + str(round(avgPercentageChangeUSD, 2)) + '%*'
            telegramMsgs.append(message)

        else:
            currentAvgBuyPriceUSD = avgBuyPrices[1]
            previousAvgBuyPriceUSD[crypto] = currentAvgBuyPriceUSD
            avgPercentageChangeUSD = 0

        if (telegramFlag):
            if (abs(avgPercentageChangeAUD) > 5 or abs(avgPercentageChangeUSD) > 5):
                telegramMsgs.append('')
                alertMessage = TELEGRAM_USERS
                telegramMsgs.append(alertMessage)

            telegramMessage = ''
            for message in telegramMsgs:
                telegramMessage += message + '\n'

            send_to_telegram(bot, chatId, telegramMessage)

        print('')


# Send message to Telegram.
def send_to_telegram(bot, chatId, message):
    bot.send_message(chat_id=chatId, 
                    text=message, 
                    parse_mode=telegram.ParseMode.MARKDOWN)


#################################################################################################
#                                       MAIN                                                    #
#################################################################################################    

global previousAvgBuyPriceAUD
global previousAvgBuyPriceUSD

config = configparser.ConfigParser()
config.read('config.ini')

telegramFlag = True
if (telegramFlag):
    token = config['TELEGRAM']['Token']
    chatId = config['TELEGRAM']['Chat_Id']

    # Initialise Telegram Bot.
    bot = telegram.Bot(token=token)
    bot.send_message(chat_id=chatId, 
                    text="Cryptocurrencies supported: \n - BTC/AUD\n - ETH/AUD\n - LTC/AUD\n - BCH/AUD\n - XRP/AUD", 
                    parse_mode=telegram.ParseMode.MARKDOWN)

previousAvgBuyPriceAUD = {
                            "BTC": 0,
                            "ETH": 0,
                            "LTC": 0,
                            "BCH": 0,
                            "XRP": 0
                         }
previousAvgBuyPriceUSD = previousAvgBuyPriceAUD.copy()
while True:
    if (telegramFlag):
        display_crypto_prices(telegramFlag, bot, chatId)

    else:
        display_crypto_prices(telegramFlag, '', '')

    # Sleep for t seconds (30 minutes).
    sleep(1800)