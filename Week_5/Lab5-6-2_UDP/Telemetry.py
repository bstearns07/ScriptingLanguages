############################################################################################################
# Title: Lab 5.6.2 - UDP Telemetry
# Author: Ben Stearns
# Date: 9-17-2025
# Description: Simulates sending telemetry temperature and humidity data to a network
############################################################################################################

import socket, time, random
attemptNumber = 1 # to keep track of attempt during timeout exceptions

# only attempt the connection a maximum of 2 times
while attemptNumber < 3:
    try:
        # Define a UDP ipV4 socket object with a timeout of 1 second
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(1.0)

            # create 5 random temperature and humidity values. Use these values to create messages to send to the sever
            for i in range(5):
                temp = round(70 + random.random()*5, 2)
                humidity = random.randint(0,100)
                tempMsg = f"temp {temp}".encode("utf-8")
                humidityMsg = f"humidity {humidity}".encode("utf-8")

                # attempt to send values to the server, then store and print the response
                sock.sendto(tempMsg, ("127.0.0.1", 9000))
                sock.sendto(humidityMsg, ("127.0.0.1", 9000))

                # store the data and address information sent back from the network
                data, addr = sock.recvfrom(1024)
                time.sleep(1) # so each transmission takes a second per instructions

                # print the server response by decoding from byte form back to a string
                # ignore bytes that are not valid utf format to prevent decoding exceptions from occurring
                print(f"Sent {tempMsg.decode("utf-8",errors="ignore")}, got reply:", data.decode("utf-8",errors="ignore"))
                print(f"Send {humidityMsg.decode("utf-8",errors="ignore")}, got reply: ",data.decode("utf-8",errors="ignore"))

            # once all 5 data sets are sent, break from the while loop
            break
    # If a timeout occurs, check what the attempt number is
    # If on only the first attempt, say "attempting to retry", increment variable, and allow while loop to continue
    # Otherwise print "ending program" and break the while loop
    except socket.timeout:
        if attemptNumber == 1:
            print("Timeout occurred. Attempting to retry...")
            attemptNumber += 1
            time.sleep(1) # as per instructions
        else:
            print("Timeout occurred. Ending program...")
            break
    # catch all other exceptions and print. Then break the while loop
    except Exception as e:
        print(f"Exception occurred: {e}")
        break