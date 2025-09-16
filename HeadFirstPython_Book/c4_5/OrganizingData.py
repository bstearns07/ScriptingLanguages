import swimclub
import pprint
import os
import webbrowser
# create empty dictionary for storing each unique swimmer name
swimmers = {}

# store all the swim data files and remove .DS.Store if it's there
swim_files = os.listdir(swimclub.FOLDER)
if ".DS_Store" in swim_files:
    swim_files.remove(".DS_Store")

# loop through files and append the swimmer names to the dictionary as a key if not already in dictionary
for file in swim_files:

    # store data from the file using ReadSwimData function
    name, *_ = swimclub.Read_Swim_Data(file)

    # add name to dictionary if not already there
    if name not in swimmers:
        swimmers[name] = []
    swimmers[name].append(file)

for filename in swimmers["Calvin"]:
    webbrowser.open("file://" + os.path.realpath(swimclub.produce_bar_chart(filename)))