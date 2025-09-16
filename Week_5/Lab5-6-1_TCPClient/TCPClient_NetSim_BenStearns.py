############################################################################################################
# Title: Lab 5.6.1 - TCPClient / Net Sim
# Author: Ben Stearns
# Date: 9-16-2025
# Description: Program that simulates connecting to a network, creating a course, confirming the new course
#              is created, delete the course, and confirm deletion
############################################################################################################

import socket # used for basic network communication and port scanning

# define IP address and port for the listening network
IP = "127.0.0.1"
PORT = 7001

# creates a context manager so the socket closes once out of scope
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # set the address family to IPv4 and type to TCP
    # if operations take longer than 3 seconds, timeout and try again only once more
    # connect to the network
    s.settimeout(3.0)
    s.connect((IP, PORT))

    # send the required commands to the server one at a time
    for command in ['SET Course networking','GET Course', 'DEL networking', 'GET Course']:
        s.sendall((command + "\n").encode("utf-8")) # encodes the command string into bytes required for network communication

        # store a maximum of 1024 bytes from the server response
        # print the response by decoding the bytes received back into a string
        # skip any bytes received that aren't utf-8 to avoid decoding errors
        data = s.recv(1024)
        print("Server response: " + data.decode("utf-8",errors="ignore"))
