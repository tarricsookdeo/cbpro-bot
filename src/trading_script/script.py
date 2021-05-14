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
        price = client.get_product_ticker('BTC-USD')
        if price.ask >= take_profit or price.ask <= stop_loss:
            if config.paper_trade:
                price = price.ask
                now = datetime.now().strftime('%m-%d-%Y %H:%M:%S')
                r = requests.get('http://127.0.0.1:8000/api/v1/trades/')
                last_trade_id = r.json()[-1]['id']
                last_trade_shares = r.json[-1]['shares']
                fee = (price * last_trade_shares) * \
                    (config.taker_fee_percent / 100)
                trade = {'exit_price': price,
                         'exit_datetime': now, 'exit_fee': fee}
                url = f'http://127.0.0.1:8000/api/v1/trades/{last_trade_id}/'
                r = requests.patch(url, data=trade)
                if r.status_code == 200:
                    print(
                        f'Paper Trade Placed: ticker: BTC-USD, shares: 0.01, exit_price: {price}, exit_datetime: {now}, exit_fee: {fee}')
                    active_trade = False
                    take_profit = None
                    stop_loss = None
            else:
                pass
        time.sleep(1)
    while not active_trade:
        print('Looking for buy signal...')
        df = config.get_market_data(client, 60)

        macd_values = ta.trend.MACD(df['Close'])
        df['MACD'] = macd_values.macd()

        if df.iloc[-1]['MACD'] > 0 and df.iloc[-2]['MACD'] < 0 and df.iloc[-3]['MACD'] < 0:
            if config.paper_trade:
                price = client.get_product_ticker('BTC-USD')
                trade_logged = helpers.log_buy_order_paper_trade(price.bid)
                if trade_logged:
                    take_profit = price.bid + (price.bid * 0.02)
                    stop_loss = (price.bid * 0.99)
                    active_trade = True
            else:
                pass
        time.sleep(60)
