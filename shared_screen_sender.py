import threading
from vidstream import ScreenShareClient
import socket
import time
from utils.db_connection import get_database

db = get_database()
cursor = db.cursor()
query = "SELECT DISTINCT ip_address FROM active_user_ip WHERE user_type = 'student';"
values = ()
cursor.execute(query,)
result = cursor.fetchall()

ip_addresses = ["192.168.0.115", "192.168.137.1", 'localhost']
# ip_addresses = [r[0] for r in result]
ports = [9999, 9998, 9997, 9996, 9995]
senders = []
threads = []
connected_addresses = set()


def is_server_available(ip_address, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((ip_address, port))
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False


def create_sender(ip_address, port):
    if (ip_address, port) not in senders:
        sender = ScreenShareClient(ip_address, port)
        senders.append((ip_address, port))
        thread = threading.Thread(target=sender.start_stream)
        thread.start()


while True:
    for ip_address in ip_addresses:
        if ip_address in connected_addresses:
            continue
        for port in ports:
            if is_server_available(ip_address, port):
                connected_addresses.add(ip_address)
                create_sender(ip_address, port)
        time.sleep(1)  # wait 1 second before checking for next IP address

    if len(connected_addresses) == len(ip_addresses):
        break

    print("Not all IP addresses available. Retrying in 5 seconds...")
    time.sleep(5)


while input("") != 'STOP':
    # check if any sender has disconnected
    for sender in senders:
        if not sender[0].is_connected():
            senders.remove(sender)

    # check if any new server is available
    for ip_address in ip_addresses:
        if ip_address in connected_addresses:
            continue
        for port in ports:
            if is_server_available(ip_address, port):
                connected_addresses.add(ip_address)
                create_sender(ip_address, port)
    time.sleep(1)  # wait 1 second before checking again


for sender in senders:
    thread = threading.Thread(target=sender[0].start_stream)
    thread.start()
    threads.append(thread)


for thread in threads:
    thread.join()
