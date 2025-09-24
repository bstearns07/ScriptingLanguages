# import needed modules
import socket
import time
import random

# define the IP address and port number of listening network
IP = "127.0.0.1"
PORT = 9000

# define a socket object
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    # set a timeout of 1 second
    sock.settimeout(1.0)

    try:
        # send 5 sets of data
        for _ in range(5):
            # create a random number between 70-75 for temperature and 0-100 for humidity
            # random.random returns a random value between 0.0 and 1.0
            temp = round(70 + random.random() * 5, 2)
            humidity = random.randint(0, 100)
            # define string message in byte form to send
            tempMsg = f"Temp sent: {temp}".encode('utf-8')
            humidityMsg = f"Humidity: {humidity}".encode('utf-8')
            # send data to server
            sock.sendto(tempMsg, (IP, PORT))
            sock.sendto(humidityMsg, (IP, PORT))

            #store and print response
            data, addr = sock.recvfrom(1024)
            print(f"Sent {tempMsg.decode("utf-8", errors="ignore")}, got reply:", data.decode("utf-8", errors="ignore"))
            print(f"Send {humidityMsg.decode("utf-8", errors="ignore")}, got reply: ", data.decode("utf-8", errors="ignore"))
    except socket.timeout:
        print("Timed out")
    except Exception as error:
        print(error)
