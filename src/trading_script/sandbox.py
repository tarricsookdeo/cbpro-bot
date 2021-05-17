# Used for testing. Will not be in final product.
import cbpro
import ta

import config
import helpers

client = cbpro.AuthenticatedClient(
    config.cbpro_public_key, config.cbpro_secret_key, config.cbpro_key_passphrase)

print(helpers.get_price(client, 'BTC-USD', 'BUY'))
print(helpers.get_price(client, 'BTC-USD', 'SELL'))
