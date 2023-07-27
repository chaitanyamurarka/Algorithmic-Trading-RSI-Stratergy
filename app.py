import streamlit as st
import numpy as np
import pandas as pd
import time
import yfinance as yf
import ta

st.title("Algo Trading Strategy")

st.write("Enter the parameters:")
stock_name = st.text_input("Stock Code", "RELIANCE.NS")
lot_size = st.number_input("Lot Size", value=1, step=1)
profit_factor = st.number_input("Profit Factor", value=2, step=1)
martingale_limit = st.number_input("Martingale Limit", value=5, step=1)

# Stochastic Oscillator parameters
stoch_k_period = st.number_input("Stochastic %K Period", value=5, step=1)
stoch_d_period = st.number_input("Stochastic %D Period", value=3, step=1)
stoch_slowing = st.number_input("Stochastic Slowing", value=3, step=1)
price_field = st.selectbox("Price Field", ["Low/High", "Close/Close"])
method = st.selectbox("Method", ["Simple", "Exponential", "Smoothed", "Linear Weighted"])
overbought_level = st.number_input("Overbought Level", value=80, step=1)
oversold_level = st.number_input("Oversold Level", value=20, step=1)

# Function to place a trade (Buy or Sell)
def place_trade(order_type, lot_size, price):
    st.write(f"Placing a {order_type} order for {lot_size} lots at price {price}")

def cancel_pending():
    st.write("\nPending orders cancelled")

consecutive_losses = 0
start_button = st.button("Start")
stop_button = st.button('Stop')

while start_button:
    if stop_button:
        st.write('Program Stopped Successfully')
        break

    # Wait until the start of the next minute
    current_time = pd.Timestamp.now().time()
    seconds_to_next_minute = 62 - current_time.second
    st.write(f'Starting Program in {seconds_to_next_minute} seconds')
    time.sleep(seconds_to_next_minute)

    # Interval required 1 minute
    data = yf.download(tickers=stock_name, period='1d', interval='1m')

    # Assuming 'data' contains the historical stock data fetched using yfinance
    previous_candle = data.iloc[-2]  # Get the row for the previous candle
    st.write(previous_candle)

    # Calculate Stochastic Oscillator values
    if price_field == "Low/High":
        stoch_low = data['Low'].rolling(stoch_k_period).min()
        stoch_high = data['High'].rolling(stoch_k_period).max()
    else:  # Use Close/Close as default
        stoch_low = data['Close'].rolling(stoch_k_period).min()
        stoch_high = data['Close'].rolling(stoch_k_period).max()

    stoch_k = 100 * (data['Close'] - stoch_low) / (stoch_high - stoch_low)
    stoch_d = stoch_k.rolling(stoch_d_period).mean()

    if previous_candle['Close'] > previous_candle['Open']:
        pre_bull_or_bear = 'bull'
        st.write("Previous candle was bullish.")
        if stoch_k.iloc[-2] < oversold_level:
            # If Stochastic %K is less than the oversold level, Buy 1 lot / stock at the Close price of the previous candle.
            place_trade("Buy", lot_size, previous_candle['Close'])
        else:
            st.write(f"Stochastic %K is {stoch_k.iloc[-2]}, not in oversold range. Skipping trade.")
    else:
        st.write("Previous candle was bearish.")
        if stoch_k.iloc[-2] > overbought_level:
            # If Stochastic %K is greater than the overbought level, Sell 1 lot / stock at the Close price of the previous candle.
            place_trade("Sell", lot_size, previous_candle['Close'])
        else:
            st.write(f"Stochastic %K is {stoch_k.iloc[-2]}, not in overbought range. Skipping trade.")

    # Wait until the end of the current minute (59th second of the minute)
    current_time = pd.Timestamp.now().time()
    seconds_to_next_minute = 57 - current_time.second
    time.sleep(seconds_to_next_minute)
    cancel_pending()
    data = yf.download(tickers=stock_name, period='1d', interval='1m')
    current_candle = data.iloc[-1]

    # Continue with the rest of the code for adjusting the lot size based on profitability
    # ... (same as before)



    if pre_bull_or_bear == 'bull':
        # At the end of the candle, check if the position is profitable
        if previous_candle['Close'] < current_candle['Close']:
            # The position was profitable, reset the consecutive losses counter
            st.write("Position was profitable. Keeping lot size at 1.")
            consecutive_losses = 0
        else:
            # The position was a loss
            consecutive_losses += 1
            if consecutive_losses >= martingale_limit:
                st.write(f"Reached Martingale Limit of {martingale_limit} consecutive losses. Stopping.")
                break
            else:
                # Multiply lot size by profit_factor
                st.write("Position was a loss. Multiplying lot size by 2.")
                lot_size *= profit_factor
    else:
        # At the end of the candle, check if the position is profitable
        if previous_candle['Close'] > current_candle['Close']:
            # The position was profitable, reset the consecutive losses counter
            st.write("Position was profitable. Keeping lot size at 1.")
            consecutive_losses = 0
        else:
            # The position was a loss
            consecutive_losses += 1
            if consecutive_losses >= martingale_limit:
                st.write(f"Reached Martingale Limit of {martingale_limit} consecutive losses. Stopping.")
                break
            else:
                # Multiply lot size by profit_factor
                st.write("Position was a loss. Multiplying lot size by 2.")
                lot_size *= profit_factor