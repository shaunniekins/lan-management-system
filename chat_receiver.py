import socket
import threading
import os
import datetime

hostname = socket.gethostname()
HOST = socket.gethostbyname(hostname)
PORT = 9995

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


def receive_messages():
    LAN_FILES_DIR = os.path.expanduser("~/Documents/LAN_Files")
    if not os.path.exists(LAN_FILES_DIR):
        os.makedirs(LAN_FILES_DIR)

    while True:
        msg = client_socket.recv(1024).decode()
        print("message: ", msg)
        
        if msg == "quit":
            break

    client_socket.close()


receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()

while True:
    message = input("Message: ")
    client_socket.send(message.encode('utf-8'))
    if message == "quit":
        break
