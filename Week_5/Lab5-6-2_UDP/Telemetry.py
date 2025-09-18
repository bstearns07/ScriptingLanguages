############################################################################################################
# Title: Lab 5.6.2 - UDP Telemetry
# Author: Ben Stearns
# Date: 9-17-2025
# Description:
############################################################################################################

import socket, time, random

# Define a UDP ipV4 socket object with a timeout
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(1.0)

# create 5 random temperature and humidity values. Use values to make a message to send to the sever
for i in range(5):
    temp = round(70 + random.random()*5, 2) # random temp
    humidity = f"{random.randint(0,100)}%"
    tempMsg = f"temp {temp}".encode()
    humidityMsg = f"temp {humidity}".encode()

    # attempt to send values to the server, then store and print the response
    try:
        sock.sendto(tempMsg, ("127.0.0.1", 9000))
        sock.sendto(humidityMsg, ("127.0.0.1", 9000))
        time.sleep(1)
        data, addr = sock.recvfrom(1024)
        print(f"Sent {tempMsg}, got reply:", data.decode("utf-8",errors="ignore"))
        print(f"Send {humidity}, got reply: ",data.decode("utf-8",errors="ignore"))

    # if connection times out, try one more time
    except socket.timeout:
        print("Timeout occurred. Attempting to retry...")
        time.sleep(1)
        try:
            sock.sendto(tempMsg, ("127.0.0.1", 9000))
            sock.sendto(humidityMsg, ("127.0.0.1", 9000))
            time.sleep(1)
            data, addr = sock.recvfrom(1024)
            print(f"Sent {tempMsg}, got reply:", data.decode("utf-8",errors="ignore"))
            print(f"Send {humidity}, got reply: ",data.decode("utf-8",errors="ignore"))
        # if timeout occurs a second time, end program
        except socket.timeout:
            print("Timeout occurred. Ending program...")
