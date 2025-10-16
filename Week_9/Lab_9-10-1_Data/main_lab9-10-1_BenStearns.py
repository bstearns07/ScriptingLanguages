########################################################################################################################
# Title............: Lab 9.10.1
# Author...........: Ben Stearns
# Date.............: 10-16-2025
# Purpose..........: The purpose of this program is to:
#                       - Load movie data that was fetched and saved into as a .csv file
#                       - Establish a user menu allowing for the following functions:
#                           - Filter movies by genre
#                           - Calculating statistics for average rating and movie runtime
#                           - List top movies by rating
#                           - Visualize the data as a bar, line, and histogram chart
#                           - Exiting the application
# File Description...: defines the main program user interface for the application
#######################################################################################################################
import textwrap
from traceback import print_tb

import pandas as pd
import matplotlib.pyplot as plt # for control of figure size, subplots, and display
import seaborn as sns # data visualization tool
import create_csv_file # for retrieving movie information stored in a csv file via Open Movie Database API

# generate and load the movie data csv file as a dataframe
df = pd.read_csv(create_csv_file.CSV_FILENAME)

# variable to storing various user responses
user_response = ""

# variables storing each user menu (ignoring common whitespace. Strip the beginning newline character):
MAIN_MENU = textwrap.dedent("""
             [1] Filter by genre
             [2] Calculate stats
             [3] Show top movies
             [4] Visualize data
             [5] Exit
             """).strip()

# variable for error checking that valid user responses are made:
VALID_MAIN_MENU = ["1","2","3","4","5"]
VALID_GENRES = ["adventure","action","drama","crime","animation","comedy","biography"]

# welcome the user, display main menu, and wait for user response
print("Welcome to Ben's Stearns Movie Data App!")
print("Make your number selection:")
while user_response != "5":
    print(MAIN_MENU)
    user_response = input("> ")

    # proceed only if user entered a valid main menu option
    while user_response not in VALID_MAIN_MENU:
        print("\nInvalid entry. Please enter the number for your selection")
        user_response = input("> ")

    # determine program function based on user's main menu choice
    match user_response:
        case "1": # filter by genre
            print(f"Enter a genre: {", ".join(VALID_GENRES)}")
            user_response = input("> ").strip().lower()
            while user_response not in VALID_MAIN_MENU:
                print("Invalid entry. Please enter a valid genre")
                uer_response = input("> ").strip().lower()
        case "5":
            break

# thank the user for using the program!
print("\nThank you for using Ben's Stearns Movie Data App!")
print("Goodbye")

