# simulates how to communicate between a client by listening

import socket

# identifies device to communicate to/from
HOST = "127.0.0.1"
PORT = 5001

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"[SRV] Listening on {HOST}:{PORT}")
    conn, addr = s.accept()
    with conn:
        print(f"[SRV] Connected by {addr}")
        conn.settimeout(10.0)  # basic hardening: no endless blocks AKA "stalls"
        while True:
            try:
                data = conn.recv(1024) #bit
                if not data:
                    break
                text = data.decode("utf-8", errors="ignore")
                if len(text) > 256:
                    conn.sendall(b"ERR: input too long\n")
                    continue
                conn.sendall(f"ECHO:{text}".encode("utf-8"))
            except socket.timeout:
                print("[SRV] Timeout; closing connection.")
                break
            except Exception as e:
                print("[SRV] Error:", e)
                break
