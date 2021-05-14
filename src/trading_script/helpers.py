from datetime import datetime

import cbpro
import pandas as pd
import requests
import ta

import config

client = cbpro.AuthenticatedClient(
    config.cbpro_public_key, config.cbpro_secret_key, config.cbpro_key_passphrase)


def log_buy_order_paper_trade(price):
    ''' Logs a new buy order to the API used to keep track of the trades.

        Arguments:

        price (decimal) - The price of the asset when bought. Precise to 6 
        decimal places.

        Returns:

        Prints a message on success or failure as well as returns a boolean
        value.

        A boolean value:
        True - if the trade was successfully logged.
        False - if there was an error while logging the trade.
    '''

    # Creates a timestanp for the current datetime.
    # the format is specifc to the API that will log the trade.
    now = datetime.now().strftime('%m-%d-%Y %H:%M:%S')
    fee = (price * config.shares) * (config.taker_fee_percent / 100)

    # Constructs a trade object using different data sources
    # such as the config file, and arguments to the method.
    trade = {'ticker': config.ticker,
             'shares': config.shares, 'entry_price': price,
             'entry_datetime': now, 'filled': True, 'entry_fee': fee}

    # Construct the url endpoint for the API request.
    url = f'{config.base_url}/trades/'

    try:
        # Makes the post request using the requests library.
        r = requests.post(url, data=trade)

        if r.ok:
            print(f'Placed buy order for {config.ticker} @ {price}')
            return True
    except:
        print('An error occured when logging the trade')
        return False


def get_market_data(cbpro_client, candle_timeframe):
    ''' Gets the OHLC candlesticks for a specified timeframe and
        returns a pandas dataframe of this data with the timestamp
        as the index.

        Arguments:

        cbpro_client (object) - A client object setup using the cbpro package.
        This should be an authenticated client setup by using cbpro.AuthenticatedClient. 
        Note that to setup an authenticated client, a public key, secret key, and 
        passphrase are needed. See cbpro documention for more details.

        cande_timeframe (int) - Represents the candlestick timeframe in seconds. For
        example, the 1 minute candle would be 60. Note that this value must be one that
        is supported by Coinbase Pro. The following are supported values: 60, 300, 900,
        3600, 21600, 86400.

        Returns:

        A pandas dataframe with columns of [Time, Low, High, Open, Close, Volume].
        Each row in the dataframe represents a single candle of it's timeframe. Note
        that the Time column will be the index in the returned dataframe. Each dataframe
        will have 300 rows by default.

        Example of a returned dataframe:

    '''

    # Get candle data from Coinbase API
    candles = cbpro_client.get_product_historic_rates(
        product_id=config.ticker, granularity=candle_timeframe)

    # Reverse the order of the candles so it can be proccessed by
    # the ta library better
    candles = candles[::-1]

    df = pd.DataFrame(candles, columns=[
        'Time', 'Low', 'High', 'Open', 'Close', 'Volume'])

    df.set_index('Time', inplace=True)

    return df


data = get_market_data(client, 60)
print(data)


def calculate_fee(price):
    ''' Calculates the fee for the trade based on the price, shares, and fee percent.

        Arguments:

        price (decimal) - the price that the order was placed at.

        Returns:

        A decimal value of the calculated fee.
    '''
    return (price * config.shares) * (config.fee_percent / 100)
