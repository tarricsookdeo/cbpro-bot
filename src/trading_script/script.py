import time
from datetime import datetime

import cbpro
import pandas as pd
import requests
import ta

import config
import helpers

client = cbpro.AuthenticatedClient(
    config.cbpro_public_key, config.cbpro_secret_key, config.cbpro_key_passphrase)

active_trade = False
take_profit = None
stop_loss = None

while True:
    while active_trade:
        print(
            f'Looking for sell signal: take profit: {take_profit} - stop loss: {stop_loss}')
        price = helpers.get_price(client, config.ticker, 'SELL')
        if price >= take_profit or price <= stop_loss:
            if config.paper_trade:
                trade_logged = helpers.log_sell_order_paper_trade(price)
                if trade_logged:
                    active_trade = False
                    take_profit = None
                    stop_loss = None
        time.sleep(1)
    while not active_trade:
        df = helpers.get_market_data(client, 60)
        df = helpers.calculate_technical_indicators(df)
        helpers.print_buy_message(df)

        if helpers.buy_signal(df):
            if config.paper_trade:
                price = helpers.get_price(client, 'BUY')
                trade_logged = helpers.log_buy_order_paper_trade(price)
                if trade_logged:
                    take_profit = price + (price * 0.02)
                    stop_loss = (price * 0.99)
                    active_trade = True
        time.sleep(60)
