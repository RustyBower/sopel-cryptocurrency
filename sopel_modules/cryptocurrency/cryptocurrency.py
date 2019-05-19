# coding=utf-8
# Copyright 2017 Rusty Bower
# Licensed under the Eiffel Forum License 2
import arrow
import datetime
import json
import requests

from sopel.module import commands, example, NOLIMIT

# List of valid currencies - https://coinmarketcap.com/api/
CURRENCIES = ["AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK", "EUR", "GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY", "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PKR", "PLN", "RUB", "SEK", "SGD", "THB", "TRY", "TWD", "ZAR"]


def display(bot, data, currency):
    name = data['name']
    # if price > $1, round to 2 decimals
    if float(data['price_{currency}'.format(currency=currency.lower())]) > 1:
        price = round(float(data['price_{currency}'.format(currency=currency.lower())]), 2)
    else:
        price = data['price_{currency}'.format(currency=currency.lower())]
    last_updated = arrow.get(datetime.datetime.utcfromtimestamp(int(data['last_updated'])).strftime('%Y-%m-%d %H:%M:%S UTC')).humanize()
    bot.say('{name} - {price} {currency} (Last Updated: {last_updated})'.format(name=name, price=price, currency=currency.upper(), last_updated=last_updated))


def get_rate(bot, crypto, currency='USD'):
    data = None
    # Ensure we are querying on a valid currency
    if currency.upper() in CURRENCIES or currency.upper() == 'USD':
        try:
            data = requests.get('https://api.coinmarketcap.com/v1/ticker/{crypto}/?convert={currency}'.format(crypto=crypto, currency=currency)).json()[0]
            return data
        except Exception:
            raise


@commands('btc', 'bitcoin')
@example('.btc')
@example('.btc USD')
def bitcoin(bot, trigger):
    # Set default currency to USD
    currency = trigger.group(2) or 'USD'
    # Get data from API
    data = get_rate(bot, 'bitcoin', currency)
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
    data = get_rate(bot, 'dogecoin', currency)
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
    data = get_rate(bot, 'ethereum', currency)
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
    data = get_rate(bot, 'litecoin', currency)
    # Have the bot print the data
    if data:
        display(bot, data, currency)
