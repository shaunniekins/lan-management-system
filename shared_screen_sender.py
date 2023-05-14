import threading
from vidstream import ScreenShareClient
import socket
import time
from utils.db_connection import get_database

db = get_database()
cursor = db.cursor()
query = "SELECT DISTINCT ip_address FROM active_user_ip WHERE user_type = 'student' AND is_active=1;"
values = ()
cursor.execute(query, )
result = cursor.fetchall()

ip_addresses = [r[0] for r in result]
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


def check_active_user_ip():
    while True:
        cursor.execute(query, )
        result = cursor.fetchall()
        updated_ip_addresses = {r[0] for r in result}

        # Check for new IP addresses
        new_ip_addresses = updated_ip_addresses - connected_addresses
        for ip_address in new_ip_addresses:
            for port in ports:
                if is_server_available(ip_address, port):
                    connected_addresses.add(ip_address)
                    create_sender(ip_address, port)

        # Check for disconnected IP addresses
        disconnected_ip_addresses = connected_addresses - updated_ip_addresses
        for ip_address in disconnected_ip_addresses:
            connected_addresses.remove(ip_address)

        time.sleep(5)  # Wait 5 seconds before checking for updates again


# Start the initial check
check_active_user_ip_thread = threading.Thread(target=check_active_user_ip)
check_active_user_ip_thread.start()

while input("") != 'STOP':
    # check if any sender has disconnected
    for sender in senders:
        if not sender[0].is_connected():
            senders.remove(sender)

    # check if any new server is available
    cursor.execute(query, )
    result = cursor.fetchall()
    updated_ip_addresses = {r[0] for r in result}

    new_ip_addresses = updated_ip_addresses - connected_addresses
    for ip_address in new_ip_addresses:
        for port in ports:
            if is_server_available(ip_address, port):
                connected_addresses.add(ip_address)
                create_sender(ip_address, port)

    time.sleep(1)  # wait 1 second before checking again

# Stop the periodic check
check_active_user_ip_thread.join()

for sender in senders:
    thread = threading.Thread(target=sender[0].start_stream)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()