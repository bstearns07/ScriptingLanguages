import statistics
FOLDER = "swimdata/"
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
    average_total_seconds, average_hundredths = str(round(average / 100, 2)).split(".")
    average_total_seconds = int(average_total_seconds)
    average_minutes = average_total_seconds // 60
    average_seconds = average_total_seconds - (average_minutes * 60)
    average_string = f"{average_minutes}:{average_seconds}.{average_hundredths}"
    return swimmer, age, distance, stroke, times, average_string, converted_times