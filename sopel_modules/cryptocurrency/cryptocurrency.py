# coding=utf-8
# Copyright 2017 Rusty Bower
# Licensed under the Eiffel Forum License 2
import arrow
import json

from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

from sopel.formatting import color, colors
from sopel.module import commands, example

# List of valid currencies - https://coinmarketcap.com/api/
CURRENCIES = [
    "AUD",
    "BRL",
    "CAD",
    "CHF",
    "CLP",
    "CNY",
    "CZK",
    "DKK",
    "EUR",
    "GBP",
    "HKD",
    "HUF",
    "IDR",
    "ILS",
    "INR",
    "JPY",
    "KRW",
    "MXN",
    "MYR",
    "NOK",
    "NZD",
    "PHP",
    "PKR",
    "PLN",
    "RUB",
    "SEK",
    "SGD",
    "THB",
    "TRY",
    "TWD",
    "ZAR",
]


def display(data, crypto, currency):
    if data["status"]["error_code"] != 0:
        message = "Could not fetch data about {}".format(crypto)
        print(message + ": " + data["status"]["error_message"])
        return message

    price = data["data"][crypto.upper()]["quote"][currency.upper()]["price"]
    percent_change_1h = data["data"][crypto.upper()]["quote"][currency.upper()][
        "percent_change_1h"
    ]
    last_updated = data["data"][crypto.upper()]["quote"][currency.upper()][
        "last_updated"
    ]

    message = "{crypto} ${price:g} "

    if percent_change_1h >= 0:
        message += color("({percent_change_1h:.2f}%)", colors.GREEN)
        message += color("\u2b06", colors.GREEN)
    else:
        message += color("({percent_change_1h:.2f}%)", colors.RED)
        message += color("\u2b07", colors.RED)

    message += " (Last Updated: {last_updated})"

    message = message.format(
        crypto=crypto.upper(),
        price=float(price),
        percent_change_1h=float(percent_change_1h),
        last_updated=arrow.get(last_updated).humanize(),
    )

    print(message)

    return message


def get_rate(bot, crypto, currency="USD"):
    data = None
    # Ensure we are querying on a valid currency
    if currency.upper() in CURRENCIES or currency.upper() == "USD":
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        parameters = {
            "symbol": crypto.upper(),
            "convert": currency.upper(),
        }
        headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": "c2cc882d-a4e4-4f2f-8cec-39633ff652cc",
        }
        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            # data = json.loads(response.text)
            data = response.json()
            return display(data, crypto, currency)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
            raise
    else:
        raise "Invalid currency"


@commands("btc", "bitcoin")
@example(".btc")
@example(".btc USD")
def bitcoin(bot, trigger):
    # Set default currency to USD
    currency = trigger.group(2) or "USD"
    # Get data from API
    bot.say(get_rate(bot, "btc", currency))


@commands("doge", "dogecoin")
@example(".doge")
@example(".doge USD")
def dogecoin(bot, trigger):
    # Set default currency to USD
    currency = trigger.group(2) or "USD"
    # Get data from API
    bot.say(get_rate(bot, "doge", currency))


@commands("eth", "ethereum")
@example(".eth")
@example(".eth USD")
def ethereum(bot, trigger):
    # Set default currency to USD
    currency = trigger.group(2) or "USD"
    # Get data from API
    bot.say(get_rate(bot, "eth", currency))


@commands("ltc", "litecoin")
@example(".ltc")
@example(".ltc USD")
def litecoin(bot, trigger):
    # Set default currency to USD
    currency = trigger.group(2) or "USD"
    # Get data from API
    bot.say(get_rate(bot, "ltc", currency))


@commands("coin", "cryptocoin")
@example(".coin MATIC")
@example(".coin MATIC USD")
def coin(bot, trigger):
    coin = trigger.group(3) or "BTC"
    # Set default currency to USD
    currency = trigger.group(4) or "USD"
    # Get data from API
    bot.say(get_rate(bot, coin.lower(), currency))
