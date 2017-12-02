# coding=utf-8
# Copyright 2017 Rusty Bower
# Licensed under the Eiffel Forum License 2
import datetime
import json
import requests

from sopel.module import commands, example, NOLIMIT

# List of valid currencies - https://coinmarketcap.com/api/
CURRENCIES = ["AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK", "EUR", "GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY", "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PKR", "PLN", "RUB", "SEK", "SGD", "THB", "TRY", "TWD", "ZAR"]


def display(bot, data, currency):
    name = data['name']
    price = data['price_{currency}'.format(currency=currency.lower())]
    last_updated = datetime.datetime.utcfromtimestamp(int(data['last_updated'])).strftime('%Y-%m-%d %H:%M:%S UTC')
    bot.say('{name} - {price} {currency} (Last Updated: {last_updated})'.format(name=name, price=price, currency=currency.upper(), last_updated=last_updated))


def get_rate(bot, symbol, currency='USD'):
    data = None
    symbol = symbol.upper()
    # Ensure we are querying on a valid currency
    if currency.upper() in CURRENCIES or currency.upper() == 'USD':
        if symbol == 'BTC':
            try:
                data = requests.get('https://api.coinmarketcap.com/v1/ticker/bitcoin/?convert={currency}'.format(currency=currency)).json()[0]
                return data
            except Exception:
                bot.say('ERROR: Something went wrong while I was getting the exchange rate.')
                return False
        elif symbol == 'DOGE':
            try:
                data = requests.get('https://api.coinmarketcap.com/v1/ticker/dogecoin/?convert={currency}'.format(currency=currency)).json()[0]
                return data
            except Exception:
                bot.say('ERROR: Something went wrong while I was getting the exchange rate.')
                return False
        elif symbol == 'ETH':
            try:
                data = requests.get('https://api.coinmarketcap.com/v1/ticker/ethereum/?convert={currency}'.format(currency=currency)).json()[0]
                return data
            except Exception:
                bot.say('ERROR: Something went wrong while I was getting the exchange rate.')
                return False
        elif symbol == 'LTC':
            try:
                data = requests.get('https://api.coinmarketcap.com/v1/ticker/litecoin/?convert={currency}'.format(currency=currency)).json()[0]
                return data
            except Exception:
                bot.say('ERROR: Something went wrong while I was getting the exchange rate.')
                return False
        else:
            bot.say('ERROR: Unsupported Symbol')
    else:
        bot.say('ERROR: Invalid Currency')
        bot.say('Allowed Currencies: {currencies}'.format(currencies=', '.join(CURRENCIES)))
        return False


@commands('btc', 'bitcoin')
@example('.btc')
@example('.btc USD')
def bitcoin(bot, trigger):
    # Set default currency to USD
    currency = trigger.group(2) or 'USD'
    # Get data from API
    data = get_rate(bot, 'btc', currency)
    # Have the bot print the data
    if data:
        display(bot, data, currency)


@commands('doge', 'dogecoin')
@example('.doge')
@example('.doge USD')
def dogecoin(bot, trigger):
    # Set default currency to USD
    currency = trigger.group(2) or 'USD'
    # Get data from API
    data = get_rate(bot, 'doge', currency)
    # Have the bot print the data
    if data:
        display(bot, data, currency)


@commands('eth', 'ethereum')
@example('.eth')
@example('.eth USD')
def ethereum(bot, trigger):
    # Set default currency to USD
    currency = trigger.group(2) or 'USD'
    # Get data from API
    data = get_rate(bot, 'eth', currency)
    # Have the bot print the data
    if data:
        display(bot, data, currency)


@commands('ltc', 'litecoin')
@example('.ltc')
@example('.ltc USD')
def litecoin(bot, trigger):
    # Set default currency to USD
    currency = trigger.group(2) or 'USD'
    # Get data from API
    data = get_rate(bot, 'ltc', currency)
    # Have the bot print the data
    if data:
        display(bot, data, currency)
