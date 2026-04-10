# 🔐 Network Event Monitoring System

## 📌 Overview

This project is a **real-time network event monitoring system** built using Python.
It simulates a **Security Operations Center (SOC)** environment where clients send system events to a central server.

---

## ⚙️ Features

* 🔐 Secure authentication using SSL (TCP)
* 📡 Real-time event transmission using UDP
* ⚡ Edge filtering to reduce network load
* 📉 Packet loss detection using sequence numbers
* 📊 Event aggregation and statistics
* 🚨 Event classification (WARNING / CRITICAL)

---

## 🧠 Concepts Used

* Socket Programming (TCP & UDP)
* SSL/TLS Security
* Multithreading
* Event-driven architecture
* Edge computing principles

---

## 🏗️ Architecture

Client → SSL Authentication → Server
Client → UDP Events → Server Processing Engine

---

## 🚀 How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate SSL certificates

```bash
python generate_cert.py
```

### 3. Run Server

```bash
python server.py
```

### 4. Run Client

```bash
python client.py
```

---

## 📊 Example Output

```
[EVENT] Node:abc123 | Event:CPU_THRESHOLD | Severity:WARNING
CPU_THRESHOLD : 5
PACKET_DROP : 2
```

---

## 🎯 Use Cases

* Network monitoring systems
* Cybersecurity labs
* SOC simulations
* IoT event monitoring

---

## 👨‍💻 Author

Chandrakanth V G
