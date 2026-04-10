import socket
import ssl
import threading

TCP_PORT = 9000
UDP_PORT = 5005

event_count = {}
last_seq = {}

# -------- EVENT CLASSIFICATION --------
def classify_event(event):
    if event == "CPU_THRESHOLD":
        return "WARNING"
    elif event == "PACKET_DROP":
        return "CRITICAL"
    elif event == "MEMORY_THRESHOLD":
        return "WARNING"
    else:
        return "INFO"


# -------- SSL AUTH SERVER --------
def handle_client(conn, addr):
    print(f"[SSL CONNECTED] {addr}")
    try:
        data = conn.recv(1024).decode()
        print("Auth:", data)

        conn.send("AUTH_SUCCESS".encode())

    except Exception as e:
        print("Error:", e)

    finally:
        conn.close()


def start_ssl_server():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain("certs/cert.pem", "certs/key.pem")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(("0.0.0.0", TCP_PORT))
    sock.listen(5)

    print("SSL Server running on port 9000")

    while True:
        client, addr = sock.accept()
        conn = context.wrap_socket(client, server_side=True)

        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


# -------- UDP SERVER --------
def start_udp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(("0.0.0.0", UDP_PORT))
    print("UDP Server running on port 5005")

    while True:
        data, addr = sock.recvfrom(1024)

        try:
            node, event, seq = data.decode().split("|")
            seq = int(seq)

            # -------- PACKET LOSS --------
            if node in last_seq:
                if seq != last_seq[node] + 1:
                    print(f"[LOSS] Packet loss detected for {node}")

            last_seq[node] = seq

            # -------- CLASSIFICATION --------
            severity = classify_event(event)

            # -------- AGGREGATION --------
            event_count[event] = event_count.get(event, 0) + 1

            print(f"[EVENT] Node:{node} | Event:{event} | Severity:{severity}")

            print("---- Stats ----")
            for e, count in event_count.items():
                print(e, ":", count)
            print("----------------")

        except:
            print("Invalid packet")


# -------- MAIN --------
if __name__ == "__main__":
    threading.Thread(target=start_ssl_server, daemon=True).start()
    start_udp_server()