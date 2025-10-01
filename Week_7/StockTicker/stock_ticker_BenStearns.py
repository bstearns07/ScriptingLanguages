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
import matplotlib # to plot data into a chart
import logging # to access and silence any unnecessary logging information printed to the console by yfinance

# get user input
user_input = input("Enter any number stock ticker symbols: ").split(' ')
print(f"Retrieving data for {user_input}...\n")

# Silence yfinance logging
logging.getLogger("yfinance").setLevel(logging.CRITICAL)

try:
    # download the data for the user's ticker symbols
    data = yf.download(user_input, auto_adjust=False, progress=False).head(5)
    # check if returned data frame is empty. Only print the data if it has rows in it
    if data.empty:
        print(f"No data was found for ticker symbol(s): {user_input}")
    else:
        print(data)
except Exception as e:
    print(f"Error: {e}")
