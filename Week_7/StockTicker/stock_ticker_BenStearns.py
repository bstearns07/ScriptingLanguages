############################################################################################################
# Title......: Lab 7.8.1 - Stock Ticker
# Author.....: Ben Stearns
# Date.......: 10-1-2025
# Description: The purpose of this program is to:
#                 - Ask the user for a stock ticker symbol
#                 - Retrieve and print the first 5 rows of data for the user's ticker symbol
#                 - Display a line chart of the closing price
############################################################################################################

# imports
import requests
from bs4 import BeautifulSoup
import yfinance as yf
import matplotlib

# get user input
user_input = input("Enter any number stock ticker symbols: ")
ticker_symbols = yf.Ticker(user_input)
input_as_list = user_input.split(' ')
print(f"Retrieving data for {user_input}...\n")
print(yf.download(input_as_list, auto_adjust=False))