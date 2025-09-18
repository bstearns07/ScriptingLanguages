############################################################################################################
# Title: Lab 5.6.1 - TCPClient / Net Sim
# Author: Ben Stearns
# Date: 9-16-2025
# Description: Program that simulates connecting to a network, creating a course, confirming the new course
#              is created, delete the course, and confirm deletion
############################################################################################################

import socket # used for basic network communication and port scanning
import time

# define IP address and port information for the listening network
IP = "127.0.0.1"
PORT = 7001
currentAttemptNumber = 1

# try the connection only a maximum of 2 times
while currentAttemptNumber < 3:
    try:
        # use "with" statement so the socket closes once out of scope
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # set the address family to IPv4 and type to TCP
            # set a timeout of 3 seconds and create the connection using the IP address and port information
            s.settimeout(3.0)
            s.connect((IP, PORT))

            # send the required commands to the server one at a time
            for command in ['SET Course networking\n','GET Course\n', 'DEL networking\n', 'GET Course\n', 'QUIT\n']:
                s.sendall(command.encode("utf-8")) # encodes the command string into bytes required for network communication

                # store the server response up to a maximum of 1024 bytes
                # print the response by decoding the bytes received back into a string
                # skip any bytes received that aren't a valid utf-8 format to avoid decoding errors
                if command == 'QUIT\n':
                    time.sleep(1)
                data = s.recv(1024)
                print("Server response: " + data.decode("utf-8",errors="ignore"))
            # break the while loop once all commands have been executed
            break
    # catch any timeout exceptions.
    # On first attempt display a "trying again" message. Otherwise, display "ending program" message
    except socket.timeout:
        if currentAttemptNumber == 1:
            print(f"Attempt {currentAttemptNumber} timed out. Attempting to re-connect...")
            currentAttemptNumber += 1
        else:
            print(f"Attempt {currentAttemptNumber} timed out. Ending program...")
            currentAttemptNumber += 1
    #catch all other exceptions and print what error happened. then break from the while loop
    except Exception as e:
        print(f"Exception occurred: {e}")
        break