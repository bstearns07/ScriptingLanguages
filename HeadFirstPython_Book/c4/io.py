import statistics

# Get data from file as a string line
fn = "Darius-13-100m-Fly.txt"
swimmer, age, distance, stroke = fn.removesuffix(".txt").split("-")
FOLDER = "swimdata/"
with open(FOLDER + fn) as file:
    lines = file.readlines()

times = lines[0].strip().split(",")
converted_times = []
for time in times:
    minutes, rest = time.split(":")
    seconds, hundredths = rest.split(".")
    converted_time = (int(minutes) * 60 * 100) + (int(seconds) * 100) + int(hundredths)
    converted_times.append(converted_time)
print(converted_times)

average = statistics.mean(converted_times)
average_total_seconds, average_hundredths = str(round(average / 100, 2)).split(".")
average_total_seconds = int(average_total_seconds)
average_minutes = average_total_seconds // 60
average_seconds = average_total_seconds - (average_minutes * 60)
print(f"Average time: {average_minutes}:{average_seconds}.{average_hundredths}")