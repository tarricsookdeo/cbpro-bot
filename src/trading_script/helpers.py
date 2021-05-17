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

                         Low      High      Open     Close     Volume
        Time                                                         
        1620986520  50473.34  50520.08  50499.89  50475.78   1.945625
        1620986580  50444.89  50491.88  50475.77  50449.63   6.775999
        1620986640  50396.96  50449.62  50449.62  50396.96   2.913923
        1620986700  50396.95  50427.67  50397.57  50417.50   3.555249
        1620986760  50417.48  50443.77  50417.50  50443.77   4.348404
        ...              ...       ...       ...       ...        ...
        1621004220  50851.52  50987.90  50851.52  50943.23  43.637102
        1621004280  50920.71  50984.30  50943.23  50984.30  21.196479
        1621004340  50937.72  50996.85  50984.30  50956.54  26.671939
        1621004400  50954.71  50988.00  50956.55  50983.13  19.064374
        1621004460  50983.12  51170.00  50983.13  51169.98  55.817577

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
