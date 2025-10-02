############################################################################################################
# Title......: Lab 7.8.1 - Stock Ticker
# Author.....: Ben Stearns
# Date.......: 10-1-2025
# Description: The purpose of this program is to:
#                 - Ask the user for any number of stock ticker symbols
#                 - Retrieve and print the first 5 rows of data for the user's ticker symbol(s)
#                 - Display a line chart of the closing prices for each ticker symbol
############################################################################################################

# imports
import requests
from bs4 import BeautifulSoup
import yfinance as yf # to retrieve finance data
import matplotlib.pyplot as plt # to plot data into a chart
import logging # to access and silence any unnecessary logging information printed to the console by yfinance

# create a list of valid time periods for error checking
valid_periods = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]

# get user input as a list in all uppercase (some functionality is case-sensitive)
tickers = input("Enter any number stock ticker symbols separated by a SPACE: ").upper().split(' ')

# ask the user what period of time to retrieve data from until a valid entry is made
while True:
    period = input("Enter the period to retrieve data for (example: 1mo, 6mo, 1y): ").lower()
    if period in valid_periods:
        break
    else:
        print(f"\nInvalid period. Please choose from: {', '.join(valid_periods)}")
print(f"\nRetrieving data for {', '.join(tickers)} going back {period}...\n")

# Silence yfinance logging
logging.getLogger("yfinance").setLevel(logging.CRITICAL)

try:
    # download the data for the user's ticker symbols
    data = yf.download(tickers, auto_adjust=False, progress=False, period=period).head(5)

    # Only print the datagram if it has rows in it
    if data.empty:
        print(f"No data was found for ticker symbol(s): {', '.join(tickers)}")
    else:
        print(data)

        # create a plot figure big enough so words don't squish together too much
        plt.figure(figsize=(8,5))

        # plot each ticker the user entered
        for ticker in tickers:
            # retrieve the closing price column data.
            # If column has no data, only plot a dummy legend entry
            closing_price_column = data["Close"][ticker]
            if closing_price_column.isna().all():
                plt.plot([], [], label=f"{ticker}: No data found. Check spelling", linestyle="--", color="gray")
            else:
                # Plot normally if data was found for the ticker
                plt.plot(closing_price_column.index, closing_price_column, label=ticker)

        # Add labels, title, and legend. Then show chart
        plt.xlabel("Date")
        plt.ylabel("Closing Price (USD)")
        plt.title("Closing Prices")
        plt.legend()
        plt.show()
# catch and print all exceptions thrown
except Exception as e:
    print(f"An error occured: {e}")
