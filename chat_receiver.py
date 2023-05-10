import socket
import threading
import os
import datetime


hostname = socket.gethostname()
HOST = socket.gethostbyname(hostname)
PORT = 9997

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


def receive_messages():
    LAN_FILES_DIR = os.path.expanduser("~/Documents/LAN_Files")
    if not os.path.exists(LAN_FILES_DIR):
        os.makedirs(LAN_FILES_DIR)

    while True:
        FILE_MARKER = "<FILE>"

        msg = client_socket.recv(1024).decode()

        header = client_socket.recv(1024).decode()
        if header.startswith("<FILE>"):
            filename, file_size = header[len("<FILE>"):].split(":")
            file_size = int(file_size)
            file_path = os.path.join(LAN_FILES_DIR, filename)
            with open(file_path, "wb") as f:
                bytes_received = 0
                while bytes_received < file_size:
                    data = client_socket.recv(1024)
                    f.write(data)
                    bytes_received += len(data)

        else:
            print(msg)

    client_socket.close()


receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()

while True:
    pass
