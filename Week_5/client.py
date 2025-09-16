import socket # for basic network communication and port scanning

# must match communicating server
HOST = "127.0.0.1"
PORT = 5001

# creates a context manager so the socket closes once out of scope
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c: # set the address family to IPv4 and type to TCP
    # set a timeout of 5 seconds to prevent operations like connecting, receiving, sending from hanging forever
    # connect to network
    c.settimeout(5.0)
    c.connect((HOST, PORT))

    for msg in ["hello", "this is a test", "bye"]:
        # convert string to byte objects (network communication requires bytes)
        # send all bytes to server until the entire message is transmitted
        c.sendall(msg.encode("utf-8"))
        print("[CLI] Sent:", msg)

        # Limit data received by to 1024 bytes and print response by decoding the receiving bytes back to a string.
        # skip any bytes that aren't valid UTF-8 to avoid decoding errors
        data = c.recv(1024)
        print("[CLI] Recv:", data.decode("utf-8", errors="ignore"))
