#########################################################################################
# Title: Lab 1.2.2
# Author: Ben Stearns
# Date: 8-19-24
# Title: Simple Problem
# Description: Application that simulates quantum computing and adding numbers to a dictionary
########################################################################################

# import random module
import random

# start an empty dictionary
particles = {}

# generate a list of 5 unique numbers that can be indexed
uniqueNumbers = set()  # sets don't allow for duplicate numbers
while len(uniqueNumbers) < 5:
    time = random.randint(100, 200)
    uniqueNumbers.add(time)
uniqueNumbers = list(uniqueNumbers)  # convert to a list to numbers to be retrieved by indexing

# generate 5 numbers between 0-1 to serve as the state of the quantum particle
index = 0 # keeps track of what index to retrieve a unique number from the uniqueNumbers list
for _ in range(5):
    # randomly generate a 0 or 1 to represent the state of the particle
    state = random.randint(0, 1)

    # store that particle state in the dictionary using the unique numbers generated in the list variable
    particles[uniqueNumbers[index]] = state
    index = index + 1  # increment the index number so the next unique number in the list is retrieved

# simulate the passage of time by printing a random number of B's
numberOfLetterBs = random.randint(100, 200)  # generate a random number between 100-200
for _ in range(numberOfLetterBs):
    print("B ", end="")

# print dictionary results
print(f"\nDictionary results: {particles}")