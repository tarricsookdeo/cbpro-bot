# Used for testing. Will not be in final product.
from time import sleep

counter = 0  # Simulate price
# Other simulated values
take_profit = None
stop_loss = None
active_trade = False
paper_trade = True

buy_signal = True
sell_signal = False

while True:
    while active_trade:
        print(
            f'take profit: {take_profit} - stop loss: {stop_loss} - active trade: {active_trade} - counter: {counter}')
        counter += 1  # Simulated price changes

        if counter >= 20:
            if paper_trade:
                take_profit = None
                stop_loss = None
                counter = 0
                active_trade = False
        sleep(1)
    while not active_trade:
        print(
            f'take profit: {take_profit} - stop loss: {stop_loss} - active trade: {active_trade} - counter: {counter}')
        counter += 1  # Simulated price changes

        if counter >= 10:
            if paper_trade:
                take_profit = 100
                stop_loss = 90
                active_trade = True
        sleep(1)


# GENERAL SKELETON LOGIC
while True:
    while active_trade:
        if sell_signal:
            if paper_trade:
                pass  # Log and place paper trade
            else:
                pass  # Log and place real trade
        else:
            pass
    while not active_trade:
        if buy_signal:
            if paper_trade:
                pass  # Log and place paper trade
            else:
                pass  # Log and place real trade
        else:
            pass
