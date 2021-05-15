# Used for testing. Will not be in final product.
import cbpro
import ta

import config
import helpers

client = cbpro.AuthenticatedClient(
    config.cbpro_public_key, config.cbpro_secret_key, config.cbpro_key_passphrase)

df = helpers.get_market_data(client, 60)

macd = ta.trend.MACD(df['Close'])

df['MACD_DIFF'] = macd.macd_diff()

print(f"{df.iloc[-1]['MACD_DIFF']}   :    -1")
print(f"{df.iloc[-2]['MACD_DIFF']}   :    -2")
print(f"{df.iloc[-3]['MACD_DIFF']}   :    -3")

# if df.iloc[-1]['MACD_DIFF'] > 0 and df.iloc[-2]['MACD_DIFF'] < 0 and df.iloc[-3]['MACD_DIFF'] < 0:

if df.iloc[-1]['MACD_DIFF'] > 0.0:
    print('yes')
if df.iloc[-2]['MACD_DIFF'] < 0.0:
    print('yes')
if df.iloc[-3]['MACD_DIFF'] < 0.0:
    print('yes')
