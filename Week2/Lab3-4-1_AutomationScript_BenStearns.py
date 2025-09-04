#########################################################################################
# Title: Lab 3.4.1
# Author: Ben Stearns
# Date: 9-4-24
# Title: Automation Script
# Description: Automates creating a folder with files and listing all files in that folder
########################################################################################

#import needed modules
from pathlib import Path
import os
import shutil

# define needed variables
files = ["data1.txt", "data2.txt", "data3.txt"]
folder = "BenStearns_prog3_4_scripting"
destination = Path(folder)
num = 1 # to write different data to each file

# if folder doesn't exist, make one
if not os.path.exists(destination):
    os.mkdir(destination)

# loop through files in list
for filename in files:
    # create a Path object for the file's location to check if it already exists
    destinationToCheck = destination / filename # appends the file location to the parent folder

    # only proceed creating the file if it doesn't already exist in the folder
    if not destinationToCheck.exists():
        # create the file and write data to it
        with open(filename, "w") as file:
            file.write(f"Data number {num}\n")
        # move the file from the parent folder to the destination folder
        shutil.move(filename, destination)

    # increment num variable just to write something different in the next file
    num += 1

# print the contents of the folder
for file in files:
    print(file)