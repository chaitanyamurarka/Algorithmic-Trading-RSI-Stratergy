Get inputs for Stock, number of stocks/lots, time frame.

1) The code will be attached to the input time frame.
2) The code waits to get triggered till a new candle (time frame) starts. For example if input is 1 minute time frame, and user enters at 45 second, the algo waits another 15 second and then starts. 
3) Once trigerred, immediately Check the previous candle (based on time frame-1 minute candle) whether it was bullish or bearish
4) If bullish, buy 1 lot / stock at LIMIT with price as Close price of previous candle. If bearish Sellshort 1 lot / stock at LIMIT with price as close price of previous candle. This happens at the beginning of the candle. If the limit price is hit, system will automatically buy/sell.
5) At the end of the candle (Say 59th second of a minute) close the position that are open(Long or Short) and delete all the unexecuted pending orders. (sometimes limit price not reached +, so orders may be pending) 
6) If the deal was a profit, then keep the lot size at 1 or if it is a loss then multiply lot /stock size by 2. The lot size of pending orders that were deleted will remain the same for the next loop.
7) When the next candle begins, repeat step 3 to 6, but with the new lot size from previous candle.

Get input of Martingale Limit - For example, if I give 5 times then after 5 losses (1,2,4,8,16) the system will stop.

If we donot open any position, then the Martingale value must not have increased.


Get the RSI Period, Overbought and Oversold indicator values (For example Period - 14, Oversold - 30, OverBought - 70)

If the RSI indicator is input, then when entering the Candle
1) If the previous candle is Bullish, then check if the RSI value (for given period-14 in our case) is less than the Oversold indicator value (In our case 30), then BUY. If not skip and wait for next candle.
2) If the previous candle is Bearish, then check if the RSI value (for given period-14 in our case) is more than the Overbought indicator value(In our case 70), then Sell. If not skip and wait for next candle.



Get the Stochiastic Oscillator details- %K, %D, Slowing, Price Field(Low/High or Close/Close), Method (Simple or Exponential or Smoothed or Linear Weighted) , Overbought and Oversold indicator values (For example %K - 5, %D - 3, Slowing - 3 , Price Field - Low/High, Method-Simple, Oversold - 20, OverBought - 80)

If the Stochiastic indicator is input, then when entering the Candle
1) If the previous candle is Bullish, then check if the Stochiastic value is less than the Oversold indicator value (In our case 20), then BUY. If not skip and wait for next candle.
2) If the previous candle is Bearish, then check if the Stochiastic value is more than the Overbought indicator value(In our case 80), then Sell. If not skip and wait for next candle.
