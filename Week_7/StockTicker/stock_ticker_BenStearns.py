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

# get user input as a list in all uppercase
tickers = input("Enter any number stock ticker symbols: ").upper().split(' ')
print(f"Retrieving data for {tickers}...\n")

# Silence yfinance logging
logging.getLogger("yfinance").setLevel(logging.CRITICAL)

try:
    # download the data for the user's ticker symbols
    data = yf.download(tickers, auto_adjust=False, progress=False).head(5)
    # check if returned data frame is empty. Only print the data if it has rows in it
    if data.empty:
        print(f"No data was found for ticker symbol(s): {tickers}")
    else:
        print(data)
        # Plot the closing numbers
        # data.index = dates on the x-axis
        # plt.plot(x-axis data, y data, format_string to control color & line style(optional), key arguments(opt)
        plt.figure(figsize=(8,5))
        for ticker in tickers:
            plt.plot(data.index, data["Close"][ticker], label=ticker)

        # Add labels, title, and legend
        plt.xlabel("Date")
        plt.ylabel("Closing Price (USD)")
        plt.title("Closing Prices")
        plt.legend()

        # Show the chart
        plt.show()
except Exception as e:
    print(f"An error occured: {e}")
