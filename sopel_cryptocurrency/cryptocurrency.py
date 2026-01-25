# coding=utf-8
# Copyright 2017 Rusty Bower
# Licensed under the Eiffel Forum License 2
from __future__ import annotations

import arrow

from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

from sopel import plugin
from sopel.config.types import StaticSection, ValidatedAttribute
from sopel.formatting import color, colors

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


class CryptocurrencySection(StaticSection):
    api_key = ValidatedAttribute("api_key", str, default="")


def setup(bot):
    bot.settings.define_section("cryptocurrency", CryptocurrencySection)


def configure(config):
    config.define_section("cryptocurrency", CryptocurrencySection)
    config.cryptocurrency.configure_setting(
        "api_key", "Enter your CoinMarketCap API key:"
    )


def display(data, crypto, currency):
    if data["status"]["error_code"] != 0:
        message = "Could not fetch data about {}".format(crypto)
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

    return message


def get_rate(bot, crypto, currency="USD"):
    if currency.upper() not in CURRENCIES and currency.upper() != "USD":
        return "Invalid currency"

    if not bot.settings.cryptocurrency.api_key:
        return "CoinMarketCap API key not configured"

    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    parameters = {
        "symbol": crypto.upper(),
        "convert": currency.upper(),
    }
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": bot.settings.cryptocurrency.api_key,
    }
    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = response.json()
        return display(data, crypto, currency)
    except (ConnectionError, Timeout, TooManyRedirects):
        return "Error connecting to CoinMarketCap API"


@plugin.command("btc", "bitcoin")
@plugin.example(".btc")
@plugin.example(".btc USD")
def bitcoin(bot, trigger):
    """Look up Bitcoin price."""
    currency = trigger.group(2) or "USD"
    bot.say(get_rate(bot, "btc", currency))


@plugin.command("doge", "dogecoin")
@plugin.example(".doge")
@plugin.example(".doge USD")
def dogecoin(bot, trigger):
    """Look up Dogecoin price."""
    currency = trigger.group(2) or "USD"
    bot.say(get_rate(bot, "doge", currency))


@plugin.command("eth", "ethereum")
@plugin.example(".eth")
@plugin.example(".eth USD")
def ethereum(bot, trigger):
    """Look up Ethereum price."""
    currency = trigger.group(2) or "USD"
    bot.say(get_rate(bot, "eth", currency))


@plugin.command("ltc", "litecoin")
@plugin.example(".ltc")
@plugin.example(".ltc USD")
def litecoin(bot, trigger):
    """Look up Litecoin price."""
    currency = trigger.group(2) or "USD"
    bot.say(get_rate(bot, "ltc", currency))


@plugin.command("coin", "cryptocoin")
@plugin.example(".coin MATIC")
@plugin.example(".coin MATIC USD")
def coin(bot, trigger):
    """Look up any cryptocurrency price."""
    coin_symbol = trigger.group(3) or "BTC"
    currency = trigger.group(4) or "USD"
    bot.say(get_rate(bot, coin_symbol.lower(), currency))
