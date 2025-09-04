import os
import swimclub
import ConvertToRange

filename = "Darius-13-100m-Fly.txt"
swimmer, age, distance, stroke, times, average, convertedTimes = swimclub.Read_Swim_Data(filename)
title = f"{swimmer} (Under {age}) {distance} {stroke}"

for time in convertedTimes:
    print(f"{time} -> {ConvertToRange.convert2range(time, 0, max(convertedTimes), 0, 400)}")

html = f""""<!DOCTYPE html>
<html>
    <head>
        <title>
            {title}
        </title>
    </head>
    <body>
        <h3>{title}</h3>
        
        <svg height="30" width="400">
            <rect height="30" width="300" style="fill:rgb(0,0,255);" />
        </svg>Label 1<br />
        <svg height="30" width="400">
            <rect height="30" width="250" style="fill:rgb(0,0,255);" />
        </svg>Label 2<br />
        <svg height="30" width="400">
            <rect height="30" width="350" style="fill:rgb(0,0,255);" />
        </svg>Label 3<br />
        <p>Average time: </p>
    </body>
</html>"""
print(html)
files = [os.listdir("swimdata/")]