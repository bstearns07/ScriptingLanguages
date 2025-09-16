import os # allows for read/write files
import webbrowser # allows for opening a webpage
import swimclub
import ConvertToRange

# assign a test filename and multi-assign value from the file
filename = "Darius-13-100m-Fly.txt"
swimmer, age, distance, stroke, times, average, convertedTimes = swimclub.Read_Swim_Data(filename)

# assign variable needed for HTML generation
title = f"{swimmer} (Under {age}) {distance} {stroke}"
from_max = max(convertedTimes) # used for scaling formula
svg = ""
convertedTimes.reverse() # so most recent swim times list first
times.reverse()

# loop through swimmer's times using enumerate for indexing
for n,t in enumerate(times,0):
    # scale the swim time down to a bar chart width of 0-350
    bar_width = ConvertToRange.convert2range(convertedTimes[n],0,from_max,0,350)

    # build a svg bar chart element from the swim time and append to svg variable
    svg += f"""
            <svg height="30" width="400">
                <rect height="30" width="{bar_width}" style="fill:rgb(0,0,255);" />
            </svg>{t}<br />
            """
# build the full html
html = f""""<!DOCTYPE html>
<html>
    <head>
        <title>
            {title}
        </title>
    </head>
    <body>
        <h3>{title}</h3>
        {svg}
        <p>Average time: {average}</p>
    </body>
</html>"""

# define a file location for the html file, write the html to the file, and open in a web browser
save_to = f"Charts/{filename.removesuffix(".txt")}.html"
with open(save_to,"w") as sf:
    print(html, file=sf)

webbrowser.open("file://" + os.path.realpath(save_to))