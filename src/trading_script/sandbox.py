# Used for testing. Will not be in final product.
import cbpro

import config
import helpers

client = cbpro.AuthenticatedClient(
    config.cbpro_public_key, config.cbpro_secret_key, config.cbpro_key_passphrase)

candles = helpers.get_market_data(client, 60)
candles_with_indicators = helpers.calculate_technical_indicators(candles)

print(candles.tail(10))
print(candles_with_indicators.tail(10))
