from socket import socket, gethostbyname, gethostname
from threading import Thread
from zlib import compress
import time
from utils.db_connection import get_database
import tkinter as tk


from mss import mss

db = get_database()
cursor = db.cursor()
query = "SELECT DISTINCT ip_address FROM active_user_ip WHERE user_type = 'student' AND is_active=1;"
values = ()
cursor.execute(query, )
result = cursor.fetchall()

ip_addresses = [r[0] for r in result]
ports = [9997]
senders = []
threads = []
connected_addresses = set()



root = tk.Tk()
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()
root.destroy()

# WIDTH = 1900
# HEIGHT = 1000


def retrieve_screenshot(conn):
    with mss() as sct:
        # The region to capture
        rect = {'top': 0, 'left': 0, 'width': WIDTH, 'height': HEIGHT}

        while 'recording':
            # Capture the screen
            img = sct.grab(rect)
            # Tweak the compression level here (0-9)
            pixels = compress(img.rgb, 6)

            # Send the size of the pixels length
            size = len(pixels)
            size_len = (size.bit_length() + 7) // 8
            conn.send(bytes([size_len]))

            # Send the actual pixels length
            size_bytes = size.to_bytes(size_len, 'big')
            conn.send(size_bytes)

            # Send pixels
            conn.sendall(pixels)


def main(ports):
    for port in ports:
        for ip_address in ip_addresses:
            try:
                sock = socket()
                sock.bind((ip_address, port))
                sock.listen(5)
                print(f'Server started at {ip_address}:{port}')

                while 'connected':
                    conn, addr = sock.accept()
                    print('Client connected IP:', addr)
                    thread = Thread(target=retrieve_screenshot, args=(conn,))
                    thread.start()

                sock.close()
            except Exception as e:
                print(f"Error: {e}")
                continue


if __name__ == '__main__':
    main(ports)
