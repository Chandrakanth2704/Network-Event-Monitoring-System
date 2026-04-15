import socket
import ssl
import threading
import datetime

TCP_PORT = 9000
UDP_PORT = 5005

# Store last sequence per client
last_seq = {}
stats = {}
last_event = {}

# ---------------- TCP (SSL AUTH SERVER) ---------------- #
def ssl_server():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

    try:
        context.load_cert_chain(certfile="certs/cert.pem", keyfile="certs/key.pem")
    except Exception as e:
        print("❌ SSL ERROR:", e)
        return

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("0.0.0.0", TCP_PORT))
    sock.listen(5)

    print(f"🔐 SSL Server running on port {TCP_PORT}")

    while True:
        client_sock, addr = sock.accept()
        try:
            conn = context.wrap_socket(client_sock, server_side=True)

            data = conn.recv(1024).decode()
            print(f"[SSL CONNECTED] {addr} -> {data}")

            conn.send("AUTH_SUCCESS".encode())
            conn.close()

        except Exception as e:
            print("SSL Connection Error:", e)


# ---------------- UDP EVENT SERVER ---------------- #
def udp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", UDP_PORT))

    print(f"📡 UDP Server running on port {UDP_PORT}")

    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode()

        try:
            node, event, seq = message.split("|")
            seq = int(seq)

            time_now = datetime.datetime.now().strftime("%H:%M:%S")

            # Packet loss detection
            if node in last_seq and seq != last_seq[node] + 1:
                print(f"[{time_now}] ❗ PACKET LOSS detected for Node {node}")
                stats["PACKET_DROP"] = stats.get("PACKET_DROP", 0) + 1

            last_seq[node] = seq

            # Duplicate event filtering (avoid spam)
            if node in last_event and last_event[node] == event:
                continue
            last_event[node] = event

            # Classification
            severity = "WARNING"
            if event == "PACKET_DROP":
                severity = "CRITICAL"
            elif event == "CPU_THRESHOLD":
                severity = "WARNING"
            elif event == "MEMORY_OVERFLOW":
                severity = "CRITICAL"

            # Print event
            print(f"[{time_now}] Node:{node} | Event:{event} | Severity:{severity}")

            # Aggregation
            stats[event] = stats.get(event, 0) + 1

            # Save to log file
            with open("log.txt", "a") as f:
                f.write(f"{time_now},{node},{event},{severity}\n")

            # Display stats
            print("---- Stats ----")
            for k, v in stats.items():
                print(f"{k} : {v}")

        except Exception as e:
            print("❌ Invalid message received:", message)


# ---------------- MAIN ---------------- #
t1 = threading.Thread(target=ssl_server)
t2 = threading.Thread(target=udp_server)

t1.start()
t2.start()
