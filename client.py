import socket
import ssl
import time
import random

SERVER_IP = "10.172.139.191"
TCP_PORT = 9000
UDP_PORT = 5005

node_id = str(random.randint(100000,999999))
seq = 0

def ssl_auth():
    context = ssl._create_unverified_context()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn = context.wrap_socket(sock)

    conn.connect((SERVER_IP, TCP_PORT))
    conn.send(f"CLIENT_{node_id}".encode())

    print("Server:", conn.recv(1024).decode())
    conn.close()

def send_events():
    global seq
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        cpu = random.randint(1,100)

        if cpu > 85:
            seq += 1
            msg = f"{node_id}|CPU_THRESHOLD|{seq}"
            sock.sendto(msg.encode(), (SERVER_IP, UDP_PORT))
            print("Sent:", msg)

        time.sleep(2)

ssl_auth()
send_events()