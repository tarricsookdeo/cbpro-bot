# Coinbase Pro Trading Bot

## Overview: This is a simple trading bot that works on Coinbase Pro.

## Requirements:

1. python 3.9+
2. npm 6.14+
3. node 10.19+
4. pipenv 11.9+

## Installation:

1. Clone the project..
2. While inside of the `cbpro-bot` folder, run `pipenv install`.
3. `cd` into the `src/client` folder and run `npm install`.
4. `cd` into the `src/trading_script` folder and create a `config.py` file.
5. `config.py` is where you will store import, and sensitive data. This is why the file is not tracked.

Inside of `config.py` place the following variables:

- cbpro_public_key (string) - Your Coinbase Pro public API key.
- cbpro_secret_key (string) - Your Coinbase Pro secret API key.
- cbpro_key_passphrase (string) - Your Coinbase Pro API passphrase.
- fee_percent (decimal) - The fee percent you expect to pay per trade. On Coinbase Pro this will usually be 0.5.
- ticker (string) - The product ID to trade. For example, 'BTC-USD'.
- shares (decimal) - The amount of shares to trade per trade.
- base_url (string) - The URL for the Django API to record trades. This will usually be 'http://127.0.0.1:8000/api/v1'.
- paper_trade (bool) - True if bot should trade in paper trades, False to place real trades.
