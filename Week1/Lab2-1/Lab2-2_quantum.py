#########################################################################################
# Title: Lab 2-2
# Author: Ben Stearns
# Date: 8-19-24
# Description: Application that simulates quantum computing and adding numbers to a dictionary
########################################################################################

#import random module
import random

#start an empty dictionary
particles = {}

#generate a list of 5 unique numbers that can be indexed
uniqueNumbers = set()#sets don't allow for duplicate numbers
while len(uniqueNumbers) < 5:
    time = random.randint(100, 200)
    uniqueNumbers.add(time)
uniqueNumbers = list(uniqueNumbers)#convert to a list to numbers to be retrieved by indexing

#define a for loop that iterates 5 times
index = 0 #keeps track of index through loop
for _ in range(5):
    #randomly generate a time and state for the quantum particle and add to dictionary
    state = random.randint(0, 1)
    particles[uniqueNumbers[index]] = state
    index = index + 1

#print results
print(f"Dictionary results: {particles}")