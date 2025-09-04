import swimclub
import os

# get list of files and remove zip-added file
swim_files = os.listdir(swimclub.FOLDER)
swim_files.remove(".DS_Store")

# use multiple assignment to store file data
for num, file in enumerate(swim_files, 1):
    swimmer, age, distance, stroke, times, average = swimclub.Read_Swim_Data(file)
    print(f"{num}: Swimmer: {swimmer}", end=", ")
    print(f"Age: {age}", end=", ")
    print(f"Distance: {distance}", end=", ")
    print(f"Stroke: {stroke}", end=", ")
    print(f"Times: {times}", end=", ")
    print(f"Average time: {average}")