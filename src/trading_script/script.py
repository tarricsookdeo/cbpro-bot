import time

import cbpro
import pandas as pd
import requests
import ta
from datetime import datetime

import config

client = cbpro.AuthenticatedClient(
    config.cbpro_public_key, config.cbpro_secret_key, config.cbpro_key_passphrase)

active_trade = False
take_profit = None
stop_loss = None

while True:
    while active_trade:
        ticker = client.get_product_ticker('BTC-USD')
        if ticker.ask >= take_profit:
            pass
        elif ticker.bid <= stop_loss:
            pass
    while not active_trade:
        print('Looking for buy signal...')
        candles = client.get_product_historic_rates(
            product_id='BTC-USD', granularity=900)
        candles = candles[::-1]
        df = pd.DataFrame(candles, columns=[
            'Time', 'Low', 'High', 'Open', 'Close', 'Volume'])
        df.set_index('Time', inplace=True)

        macd_values = ta.trend.MACD(df['Close'])
        df['MACD'] = macd_values.macd()

        if df.iloc[-1]['MACD'] > 0 and df.iloc[-2]['MACD'] < 0 and df.iloc[-3]['MACD'] < 0:
            price = client.get_product_ticker('BTC-USD')
            if config.paper_trade:
                price = client.get_product_ticker('BTC-USD')
                fee = price.bid * (config.taker_fee_percent / 100)
                now = datetime.now().strftime('%m-%d-%Y %H:%M:%S')
                trade = {'ticker': 'BTC-USD', 'shares': 0.01, 'entry_price': price.bid,
                         'entry_datetime': now, 'filled': True, 'entry_fee': fee}

                r = requests.post(
                    'http://127.0.0.1:8000/api/v1/trades/', data=trade)

                if r.status_code == 200:
                    print(
                        f'Paper Trade Placed: ticker: BTC-USD, shares: 0.01, entry_price: {price.bid}, entry_datetime: {now}, filled: True, entry_fee: {fee}')
                    take_profit = (
                        ((2 + config.taker_fee_percent) / 100) + 1) * price.bid
                    stop_loss = (
                        1 - ((1 + config.taker_fee_percent) / 100)) * price.bid
                    active_trade = True
            else:
                pass
        time.sleep(900)
