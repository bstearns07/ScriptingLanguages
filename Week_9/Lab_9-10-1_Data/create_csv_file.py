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
# File Description...: defines logic for retrieving data for pre-defined movie titles using the Open Movie Database API
#######################################################################################################################

import random # to allow for random number generation
import pandas as pd # to allow for data containment and visualization
import requests # to allow the handling of api requests for retrieving movie data

# define 3 variables for csv filename, open movie database api key & a list of movies to retrieve from the database
CSV_FILENAME = "ben_stearns_movie_data.csv"
API_KEY = "825983b2"
movies = [
    "The Shawshank Redemption", "The Godfather", "The Dark Knight", "12 Angry Men", "Schindler's List",
    "The Lord of the Rings: The Return of the King", "Pulp Fiction", "The Good, the Bad and the Ugly", "Forrest Gump",
    "Inception",
    "The Matrix", "Fight Club", "The Empire Strikes Back", "The Lord of the Rings: The Fellowship of the Ring",
    "One Flew Over the Cuckoo's Nest",
    "Star Wars", "The Silence of the Lambs", "Casablanca", "Citizen Kane", "It's a Wonderful Life",
    "The Usual Suspects", "Se7en", "The Lion King", "The Terminator", "Back to the Future",
    "Pulp Fiction", "The Godfather Part II", "The Dark Knight Rises", "Gladiator", "The Prestige",
    "The Departed", "The Green Mile", "Whiplash", "The Intouchables", "The Pianist",
    "The Revenant", "The Social Network", "The Grand Budapest Hotel", "Mad Max: Fury Road", "The Wolf of Wall Street",
    "The Big Lebowski", "The Shining", "The Sixth Sense", "The Incredibles", "The Princess Bride",
    "The Truman Show", "The Breakfast Club", "The Big Short", "The Hunt for Red October", "The Bourne Identity"
]

# define an empty list for containing a list of dictionaries
movie_data = []

# define a function that performs an api request for the list of movies' data
def get_data():
    # loop through each title in the movies list to do an api request for that title's information
    for i, title in enumerate(movies, start=1): # uses i starting at 1 to keep track of how many movies have processed
        # defines the url used to search for a title's information, parse into json, and store response as a dictionary
        url=f"https://www.omdbapi.com/?t={title}&apikey={API_KEY}"
        response = requests.get(url).json() # .json() automatically converts json to dictionary format

        # if the movie was successfully found, append the information as a dictionary to the movie_data list
        if response.get("Response") == "True":
            movie_data.append({
                "Title": response.get("Title", ""), # retrieves information by key. If fails use empty string as default
                "Year": response.get("Year", ""),
                "Rating": float(response.get("imdbRating", random.uniform(1.0, 10.0))),  # randomize if needed
                # only retrieve the first genre listed using .split(,) at index [0]
                # If genre not found, use an empty string to prevent an exception from being thrown
                "Genre": response.get("Genre", "").split(",")[0] if response.get("Genre") else "",
                "Duration": response.get("Runtime", "").replace(" min", "") # remove the "min"  so data is only numeric
            })

            # Print a status update every 5 movies
            if i % 5 == 0:
                print(f"  ...still working ({i}/{len(movies)} movies processed)")

    # create a dataframe using the all the movies retrieved from the api request and save as an .csv file
    df = pd.DataFrame(movie_data)
    df.to_csv(CSV_FILENAME, index=False) # index=False means don't include the row numbers
    return CSV_FILENAME

# if this file is ran directly, perform the api search for data
if __name__ == "__main__":
    try:
        print("Creating CSV file. Please wait...")
        get_data()
        print("Movie data successfully created")
    except Exception as e:
        print(f"An error occured retrieving the online information: {e}")