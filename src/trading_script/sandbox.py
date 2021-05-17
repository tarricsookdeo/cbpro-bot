# Used for testing. Will not be in final product.
from datetime import date, datetime
import time

import cbpro
import ta

import config
import helpers

client = cbpro.AuthenticatedClient(
    config.cbpro_public_key, config.cbpro_secret_key, config.cbpro_key_passphrase)

candles = helpers.get_market_data(client, 60)
print(candles)
