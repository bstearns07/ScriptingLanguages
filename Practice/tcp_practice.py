import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 8000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(3.0)
    s.connect((IP, PORT))

    commands = ["enable","config t","hostname S1"]
    for command in commands:
        s.sendall(command.encode("utf-8"))
        data = s.recv(1024)
        print(data.decode("utf-8",errors="ignore"))