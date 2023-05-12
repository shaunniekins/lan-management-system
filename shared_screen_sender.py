import threading
from vidstream import ScreenShareClient
import socket
import time
from utils.db_connection import get_database

db = get_database()
cursor = db.cursor()
# query = "SELECT DISTINCT ip_address FROM active_user_ip WHERE user_type = 'student' AND is_active=1;"
# values = ()
# cursor.execute(query,)
# result = cursor.fetchall()

# ip_addresses = [r[0] for r in result]
ports = [9999, 9998, 9997, 9996, 9995]
senders = []
threads = []
connected_addresses = set()
timer_interval = 5000


def get_ip_addresses():
    cursor.execute("SELECT DISTINCT ip_address FROM active_user_ip WHERE user_type = 'student' AND is_active=1;")
    result = cursor.fetchall()
    return [r[0] for r in result]



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
    ip_addresses = get_ip_addresses()
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

def check_for_updates():
    while True:
        time.sleep(5) # check every 60 seconds
        new_ip_addresses = get_ip_addresses()
        if new_ip_addresses != ip_addresses:
            # update ip_addresses and create new senders if necessary
            ip_addresses = new_ip_addresses
            # rest of the code

update_timer = threading.Thread(target=check_for_updates)
update_timer.start()


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
