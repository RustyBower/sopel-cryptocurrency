# sopel-cryptocurrency

A Sopel IRC bot plugin for cryptocurrency price lookups using the CoinMarketCap API.

> **Note:** This package was previously published as `sopel-modules.cryptocurrency`.
> Please update your dependencies to use `sopel-cryptocurrency` instead.

## Installation

```bash
pip install sopel-cryptocurrency
```

## Configuration

You need a CoinMarketCap API key. Get one at https://pro.coinmarketcap.com

```ini
[cryptocurrency]
api_key = your_api_key_here
```

## Usage

```
.btc [currency]      - Bitcoin price
.eth [currency]      - Ethereum price
.ltc [currency]      - Litecoin price
.doge [currency]     - Dogecoin price
.coin <symbol> [currency] - Any cryptocurrency price
```

### Examples

```
.btc
BTC $47646.86 (0.11%) (Last Updated: a minute ago)

.eth EUR
ETH €2154.93 (-0.04%) (Last Updated: seconds ago)

.coin MATIC
MATIC $0.89 (0.14%) (Last Updated: a minute ago)
```

## Supported Currencies

USD (default), AUD, BRL, CAD, CHF, CLP, CNY, CZK, DKK, EUR, GBP, HKD, HUF, IDR, ILS, INR, JPY, KRW, MXN, MYR, NOK, NZD, PHP, PKR, PLN, RUB, SEK, SGD, THB, TRY, TWD, ZAR

## Requirements

- Sopel 8.0+
- Python 3.8+

## License

MIT License
