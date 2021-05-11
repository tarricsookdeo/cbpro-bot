from datetime import datetime

import requests

import config


def log_buy_order(price, filled, fee, cb_trade_id=None):
    ''' Logs a new buy order to the API used to keep track of the trades.

        Arguments:

        price (decimal) - The price of the asset when bought. Precise to 6 
                          decimal places.

        filled (bool) - True if the order has been filled, false otherwise.

        fee (decimal) - The fee paid for the order. Precise to 6 decimal 
                        places.

        cb_trade_id (string) - The ID Coinbase assigns the trade when it is
                               placed. Note that this defaults to None. If
                               the trade is a paper trade, there will be no
                               assigned trade ID from Coinbase.

        Returns:

        A boolean value:
        True - if the trade was successfully logged.
        False - if there was an error while logging the trade.
    '''

    # Creates a timestanp for the current datetime.
    # the format is specifc to the API that will log the trade.
    now = datetime.now().strftime('%m-%d-%Y %H:%M:%S')

    # Constructs a trade object using different data sources
    # such as the config file, and arguments to the method.
    trade = {'ticker': config.trading_pair,
             'shares': config.shares, 'entry_price': price,
             'entry_datetime': now, 'filled': filled, 'entry_fee': fee}

    # If there is a Coinbase trade ID, add it to the trade dictionary.
    if cb_trade_id:
        trade['coinbase_trade_id'] = cb_trade_id

    # Construct the url endpoint for the API request.
    url = f'{config.base_url}/trades/'

    # Makes the post request using the requests library.
    r = requests.post(url, data=trade)

    if r.status_code == 200:
        return True
    return False
