import statistics
import ConvertToRange
FOLDER = "swimdata/"
CHARTS = "Charts/"
def Read_Swim_Data(filename):
    swimmer, age, distance, stroke = filename.removesuffix(".txt").split("-")

    with open(FOLDER + filename) as file:
        lines = file.readlines()

    times = lines[0].strip().split(",")
    converted_times = []
    for time in times:
        if ":" in time:
            minutes, rest = time.split(":")
            seconds, hundredths = rest.split(".")
            converted_time = (int(minutes) * 60 * 100) + (int(seconds) * 100) + int(hundredths)
            converted_times.append(converted_time)
        else:
            seconds, hundredths = time.split(".")
            converted_time = (int(seconds) * 100) + int(hundredths)
            converted_times.append(converted_time)
    average = statistics.mean(converted_times)
    average_total_seconds, average_hundredths = f"{average / 100:.2f}".split(".")
    average_total_seconds = int(average_total_seconds)
    average_minutes = average_total_seconds // 60
    average_seconds = average_total_seconds - (average_minutes * 60)
    average_string = f"{average_minutes}:{average_seconds:0>2}.{average_hundredths}"
    return swimmer, age, distance, stroke, times, average_string, converted_times

def produce_bar_chart(filename: str,location=CHARTS):
    swimmer, age, distance, stroke, times, average, convertedTimes = Read_Swim_Data(filename)
    title = f"{swimmer} (Under {age}) {distance} {stroke}"
    from_max = max(convertedTimes)
    svg = ""
    convertedTimes.reverse()
    times.reverse()

    for n,t in enumerate(times,0):
        bar_width = ConvertToRange.convert2range(convertedTimes[n],0,from_max,0,350)
        svg += f"""
                <svg height="30" width="400">
                    <rect height="30" width="{bar_width}" style="fill:rgb(0,0,255);" />
                </svg>{t}<br />
                """

    html = f"""<!DOCTYPE html>
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
    print(html)

    save_to = f"{location}{filename.removesuffix(".txt")}.html"
    with open(save_to,"w") as sf:
        print(html, file=sf)

    return save_to