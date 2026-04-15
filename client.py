import socket
import ssl
import time
import random

SERVER_IP = "192.168.31.231"   # change if needed
TCP_PORT = 9000
UDP_PORT = 5005

node_id = str(random.randint(100000, 999999))
seq = 0

# ---------------- SSL AUTH ---------------- #
def ssl_auth():
    context = ssl._create_unverified_context()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn = context.wrap_socket(sock)

    conn.connect((SERVER_IP, TCP_PORT))
    conn.send(f"CLIENT_{node_id}".encode())

    response = conn.recv(1024).decode()
    print("✅ Server:", response)

    conn.close()


# ---------------- UDP EVENT SENDER ---------------- #
def send_events():
    global seq

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    events = ["CPU_THRESHOLD", "MEMORY_OVERFLOW", "NORMAL"]

    while True:
        time.sleep(2)

        cpu = random.randint(1, 100)
        memory = random.randint(1, 100)

        # Decide event based on values
        if cpu > 85:
            event = "CPU_THRESHOLD"
        elif memory > 90:
            event = "MEMORY_OVERFLOW"
        else:
            event = "NORMAL"

        seq += 1

        # 🔥 Simulate packet loss (VERY IMPORTANT)
        if random.random() < 0.1:   # 20% chance
            print("⚠️ Simulating packet loss...")
            seq += 1   # skip sequence

        msg = f"{node_id}|{event}|{seq}"

        sock.sendto(msg.encode(), (SERVER_IP, UDP_PORT))
        print("📤 Sent:", msg)


# ---------------- MAIN ---------------- #
if __name__ == "__main__":
    ssl_auth()
    send_events()
