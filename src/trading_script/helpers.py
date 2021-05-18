from datetime import datetime
from decimal import Decimal

import pandas as pd
import requests
import ta

import config


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
    fee = (price * config.shares) * (config.fee_percent / 100)

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
        print('An error occured when logging the buy trade')
        return False


def log_sell_order_paper_trade(price):
    ''' Logs a sell order to the API used to keep track of the trades.

        Arguments:

        price (decimal) - The price of the asset when sold. Precise to 6 
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

    # Get's a list of trades, and stores the last one in the array.
    r = requests.get('http://127.0.0.1:8000/api/v1/trades/')
    last_trade_id = r.json()[-1]['id']

    # Calculate trade fee in dollars
    fee = (price * config.shares) * (config.fee_percent / 100)

    # Construct the trade object
    trade = {'exit_price': price,
             'exit_datetime': now, 'exit_fee': fee}

    # Contruct the URL for the last trade that was placed
    url = f'http://127.0.0.1:8000/api/v1/trades/{last_trade_id}/'

    r = requests.patch(url, data=trade)

    try:
        r = requests.patch(url, data=trade)

        if r.ok:
            print(
                f'Paper Trade Placed: ticker: BTC-USD, shares: 0.01, exit_price: {price}, exit_datetime: {now}, exit_fee: {fee}')
            return True
    except:
        print('An error occured when logging the sell trade')
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

                                  Low      High      Open     Close     Volume
        Time                                                                  
        2021-05-16 18:05:00  45670.07  45899.81  45677.81  45828.62  81.345665
        2021-05-16 18:06:00  45647.40  45830.24  45828.62  45791.62  79.989579
        2021-05-16 18:07:00  45637.42  45791.62  45791.62  45643.02  53.048009
        2021-05-16 18:08:00  45604.37  45731.96  45650.01  45620.98  59.222227
        2021-05-16 18:09:00  45579.12  45646.44  45620.97  45588.63  30.779665
        ...                       ...       ...       ...       ...        ...
        2021-05-16 23:00:00  44330.22  44468.81  44454.86  44338.63  30.027006
        2021-05-16 23:01:00  44335.00  44540.00  44338.64  44530.00  20.532007
        2021-05-16 23:02:00  44490.63  44590.48  44529.99  44573.54  25.976468
        2021-05-16 23:03:00  44573.01  44636.50  44584.71  44636.50  36.545311
        2021-05-16 23:04:00  44628.62  44636.50  44636.50  44628.63   2.351744

    '''

    # Get candle data from Coinbase API
    candles = cbpro_client.get_product_historic_rates(
        product_id=config.ticker, granularity=candle_timeframe)

    # Reverse the order of the candles so it can be proccessed by
    # the ta library better. The new order will be in ascending order.
    candles = candles[::-1]

    # Converts the list of candle data to a pandas df, with their
    # respective column names
    df = pd.DataFrame(candles, columns=[
        'Time', 'Low', 'High', 'Open', 'Close', 'Volume'])

    df['Time'] = df['Time'].apply(lambda x: datetime.fromtimestamp(x))

    # Set the timestamp column as the index
    df.set_index('Time', inplace=True)

    return df


def calculate_fee(price):
    ''' Calculates the fee for the trade based on the price, shares, and fee percent.

        Arguments:

        price (decimal) - the price that the order was placed at.

        Returns:

        A decimal value of the calculated fee.
    '''
    return (price * config.shares) * (config.fee_percent / 100)


def calculate_technical_indicators(df):
    ''' Calculates technical indicators using the ta package, and adds them
        to their respected candles in the dataframe.

        Arguments:

        df (pandas dataframe) - the dataframe with the candle data. From this data,
        the technical indicators will be calculated.

        Returns:

        A pandas dataframe with the original OHLCV candle data, along with their associated
        techincal indicators added as a new column.
    '''
    macd_values = ta.trend.MACD(df['Close'])
    df['MACD_DIFF'] = macd_values.macd_diff()

    return df


def buy_signal(df):
    ''' Returns a boolean value if a buy signal was found. Used a pandas dataframe
        to calculate the buy signal based on technical or other indicators.

        Arguments:

        df (pandas dataframe) - the dataframe with OHLCV candle data, alongside any
        calculated technical indicators.

        Returns:

        A boolean value based on if a buy signal was found:
        True - A buy signal was found
        False -  No buy signal was found
    '''
    if df.iloc[-1]['MACD_DIFF'] > 0 and df.iloc[-2]['MACD_DIFF'] < 0 and df.iloc[-3]['MACD_DIFF'] < 0:
        return True
    return False


def get_price(cbpro_client, ticker, side):
    ''' Gets the current bid or ask price of the specified ticker.

        Arguments:

        cbpro_client (object) - A client object setup using the cbpro package.
        This should be an authenticated client setup by using cbpro.AuthenticatedClient. 
        Note that to setup an authenticated client, a public key, secret key, and 
        passphrase are needed. See cbpro documention for more details.

        side (string) - This should be either 'BUY' or 'SELL'. If 'BUY' the bid will be
        returned and if 'SELL'the ask will be returned.

        Returns:

        Decimal - A decimal value of the bid or ask.
    '''
    ticker = cbpro_client.get_product_ticker(config.ticker)

    if side == 'BUY':
        price = ticker['bid']
    elif side == 'SELL':
        price = ticker['ask']

    return Decimal(price)


def print_buy_message(df):
    '''Prints a message when looking for buy order.'''
    print(
        f'''--------------------------------------------------
    Looking for buy signal... 
    Current Datetime:   {datetime.now().strftime('%m-%d-%Y %H:%M:%S')}
    Current MADC Diff: -1 - {df.iloc[-1]['MACD_DIFF']}
                       -2 - {df.iloc[-1]['MACD_DIFF']}
                       -3 - {df.iloc[-1]['MACD_DIFF']}
---------------------------------------------------
    ''')
