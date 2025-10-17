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
import textwrap                 #
import pandas as pd             # to allow for data containment and visualization
import matplotlib.pyplot as plt # for control of figure size, subplots, and display
import seaborn as sns           # data visualization tool
import create_csv_file          # for retrieving movie information stored in a csv file via Open Movie Database API

# program variables
df = pd.read_csv(create_csv_file.CSV_FILENAME)  # generate and load the movie data csv file as a dataframe
user_response = ""                              # stores user's response to all prompts
                                                # for printing the main menu
MAIN_MENU = """\nMain Menu                        
-------------------
[1] Filter by genre
[2] Calculate stats
[3] Show top movies
[4] Visualize data
[5] Exit"""
VALID_MAIN_MENU = ["1","2","3","4","5"]         # for validating that the user enters a valid menu option
VALID_GENRES = ["Adventure","Action","Drama",   # for validating that the user enters a valid genre
                "Crime","Animation","Comedy",
                "Biography"]

# welcome the user, display main menu, and wait for user response
print("Welcome to Ben's Stearns Movie Data App!")

# wrap repeated logic in a while loop for as long as the user doesn't enter "5" to quit the application
while user_response != "5":
    print(MAIN_MENU)
    user_response = input("> ")

    # validate the user entered a valid main menu option before proceeding
    while user_response not in VALID_MAIN_MENU:
        print("\nInvalid entry. Please enter the number for your selection")
        user_response = input("> ")

    # match program function to the user's main menu response
    match user_response:

        # filter by genre
        case "1":
            # ask the user to enter a genre, strip and capitalize the response, and check that a valid genre was entered
            print(f"Enter a genre: {", ".join(VALID_GENRES)}")
            user_response = input("> ").strip().title()
            while user_response not in VALID_GENRES:
                print("Invalid entry. Please enter a valid genre")
                user_response = input("> ").strip().title()
            # filter the dataframe by the user's response and print the results (print only necessary columns)
            filtered_df = df[df["Genre"] == user_response]
            print(filtered_df[["Title","Genre"]])

        # Calculate Stats Menu Option
        case "2":
            average_duration = df["Duration"].mean()
            average_rating = df["Rating"].mean()
            print(f"The average duration of Ben's movies is: {average_duration:.2f} minutes")
            print(f"The average rating of Ben's movies is: {average_rating:.2f}")

        # Top Movies menu option
        case "3":
            # sort dataframe by rating in descending order and select the top 10 rows
            sorted_df = df.sort_values(by="Rating", ascending=False).head(10)
            print("Here are Ben's top 10 movies by rating!")
            print(sorted_df[["Title","Rating"]])

        # Visualize Data Menu Option
        case "4":
            # Set the plot style and figure size
            sns.set(style="whitegrid")
            plt.figure(figsize=(14, 10))
            # subplot the matplot into 3 rows and 1 column to accommodate all 3 graphs
            plt.subplot(3, 1, 1)
            # create a bar chart using the dataframe.
            sns.barplot(data=df, x='Rating', y='Genre', hue='Genre', palette='Blues')
            plt.title('Average Rating by Genre')
            plt.ylabel("Genre")
            plt.xticks(rotation=45)
            # show chart
            plt.tight_layout() # automatically adjusts spacing between subplots to prevent overlapping labels or titles
            plt.show()
        # Quit the program menu option
        case "5":
            break

# thank the user for using the program!
print("\nThank you for using Ben's Stearns Movie Data App!")
print("Goodbye")
