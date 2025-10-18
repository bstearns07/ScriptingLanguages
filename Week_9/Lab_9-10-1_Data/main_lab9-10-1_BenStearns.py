########################################################################################################################
# Title............: Lab 9.10.1 - Data
# Author...........: Ben Stearns
# Date.............: 10-16-2025
# Purpose..........: The purpose of this program is to:
#                       - Load movie data that was fetched and saved into as a .csv file
#                       - Establish a user menu allowing for the following functions:
#                           - Filter movies by genre
#                           - Calculating statistics for average rating and average movie runtime
#                           - List top 10 movies by rating
#                           - Visualize the data using bar, pie, and histogram charts
#                           - View all movies in the csv file
#                           - Exit the program
# File Description.: defines the main program user interface for the application
#######################################################################################################################
import pandas as pd                             # to allow for data containment and visualization
import matplotlib.pyplot as plt                 # for control of figure size, subplots, and display
import seaborn as sns                           # data visualization tool
import create_csv_file                          # for the .cvs filepath variable to read movie data

# program variables
df = pd.read_csv(create_csv_file.CSV_FILENAME)  # load the movie data from the csv file as a dataframe object
user_response = ""                              # stores user's response to all prompts
# for printing the main menu
MAIN_MENU = """\nMain Menu                        
-------------------
[1] Filter by genre
[2] Calculate stats
[3] Show top movies
[4] Visualize data
[5] Show All Movies
[6] Exit"""
VALID_MAIN_MENU_OPTIONS = ["1", "2", "3", "4", "5", "6"]    # for validating that the user enters a valid menu option
VALID_GENRES = ["Adventure","Action","Drama",               # for validating that the user enters a valid genre
                "Crime","Animation","Comedy",
                "Biography"]

# welcome the user, display the main menu, and wait for user to select their menu option
print("Welcome to Ben's Stearns Movie Data App!")

# wrap repeated logic in a while loop for as long as the user doesn't enter "6" to quit the application
while user_response != "6":
    print(MAIN_MENU)
    user_response = input("> ")

    # validate the user entered a valid main menu option before proceeding
    while user_response not in VALID_MAIN_MENU_OPTIONS:
        print("Invalid entry. Please enter the number for your selection")
        user_response = input("> ")

    # match program functionality to the user's main menu response
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
            print(filtered_df[["Title","Genre"]].to_string(index=False))

        # Calculate Stats Menu Option
        case "2":
            average_duration = df["Duration"].mean()
            average_rating = df["Rating"].mean()
            print(f"The average duration of Ben's movies is: {average_duration:.2f} minutes")
            print(f"The average rating of Ben's movies is: {average_rating:.2f}")

        # Top 10 Movies
        case "3":
            # sort dataframe by rating in descending order and select the top 10 rows
            sorted_df = df.sort_values(by="Rating", ascending=False).head(10)
            print("Here are Ben's top 10 movies by rating!")
            print(sorted_df[["Title","Rating"]].to_string(index=False))

        # Visualize Data as Charts
        case "4":
            # Set the style scheme and figure size for the plots
            # subplot the figure into 3 rows and 1 column to accommodate all 3 graphs
            # store result in 2 variables, so we don't lose access to the objects for easy referencing or modifications
            sns.set_theme(style="whitegrid")
            fig, axs = plt.subplots(3, 1, figsize=(15, 18))
            # Bar chart - Average rating of each genre
            sns.barplot(x="Genre", y="Rating", data=df, ax=axs[0], hue="Genre", palette='viridis', errorbar=None)
            axs[0].set_title("Average Rating")
            axs[0].set_ylabel("Rating")
            # Pie Chart - distribution by genre
            genre_counts = df["Genre"].value_counts()  # counts how many movies there are per genre
            axs[1].pie(genre_counts, labels=genre_counts.index, autopct='%1.1f%%', startangle=140)
            axs[1].axis("Equal") # Equal aspect ratio ensures that pie is drawn as a circle.
            axs[1].set_title("Distribution of Genre")
            # Histogram - Distribution of movie durations
            # bins=10: divides duration range into 10 equal intervals
            # kde=True: adds Kernel Density Estimate to chart (smooth trend line estimating distribution shape)
            sns.histplot(df["Duration"], bins=10, kde=True, color='skyblue', ax=axs[2])
            axs[2].set_title("Distribution of Movie Durations")
            axs[2].set_xlabel("Duration (minutes)")
            axs[2].set_ylabel("Frequency")
            # show chart
            plt.tight_layout() # automatically adjusts spacing between subplots to prevent overlapping labels or titles
            plt.show()

        # Show All Movies Menu Option Logic
        case "5":
            print("Alright, here are all of Ben's movies:")
            print(df.to_string())

        # Quit the program menu option
        case "6":
            break

# thank the user for using the program!
print("\nThank you for using the Ben's Stearns Movie Data App!")
print("Goodbye")
