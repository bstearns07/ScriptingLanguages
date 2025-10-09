# logs = ["OK","ERROR","OK","ERROR",]
# errors = {}
# for ab in logs:
#     if ab == "ERROR":
#         errors[ab] = errors.get(ab, 0) + 1
# print(errors)

# number 3

############################################################################################################
# Title......: Quizzes 2
# Author.....: Ben Stearns
# Date.......: 10-9-2025
# Description: The purpose of this program is to:
#                 - demonstrate using the "set" data collections to remove duplicate values from a list
############################################################################################################
sentence = "data structures and algorithm"
counts = {}
for ab in sentence.split():
    counts[ab] = counts.get(ab, 0) + 1
print(counts)
# nums = [5,10,15,20] # instantiate the list of data required
# for num in nums: # iterate through each number in the list
#     print(num, end=" ") # print the results, overriding the default newline character with an empty space to print them all on one line

# data = [1,2,2,3,4,4,5] # instantiate a list on numbers containing duplicates
# data = set(data) # cast the data as a set to remove duplicates
# print(data) #print the final result of the set variable
# student = ("Alice", 21, "Computer Science") # instantiate a tuple containing the required data
# name, age, major = student # unpack each value in the tuple and store in separate variables using multiple assignment
# print(f"Name: {name}, Age: {age}, Major: {major}") #print the value of the 3 variables
# logs = ["OK", "ERROR","OK","ERROR"] #instantiate log list
# count = 0 # used to keep track of a running count
# for log in logs: # iterates over every string in the list
#     if log == "ERROR": # if the string contains a value of "ERROR" increase the count variable by 1
#         count += 1
# print(count) # print the running count
# number = input("Enter a whole number: ") # ask the user for a number and store as a variable
# while True:
#     if number.isdigit(): # error check that the user entered a string containing only digits
#         number = int(number) # if the user entered a string of valid digits cast to an integer object for calculations
#         if number % 2 == 0: # if there in no remainder left over after dividing the user's number by 2 it's even
#             print(f"{number} is an even number.")
#             break # free to break from loop once determined as even or odd
#         else: # otherwise the number is odd
#             print(f"{number} is an odd number.")
#             break
#     else: # if the user didn't enter a string of only digits, print "invalid" and let them try again
#         number = input("Invalid entry. Please enter a whole number: ")
# import matplotlib.pyplot as plt
# prices = [150,152,149,153,155]
# days = [1,2,3,4,5]
# plt.plot(days, prices)
# plt.title("Prices Graph")
# plt.show()