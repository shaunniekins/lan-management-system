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

        if msg.startswith("<FILE>"):
            # The message contains file data
            filename_start = msg.find("<FILE>") + len("<FILE>")
            filename_end = msg.find("<FILE>", filename_start)
            filename = msg[filename_start:filename_end]

            current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            new_filename = f"{current_time}_{os.path.basename(filename)}"
            file_contents = b""
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                file_contents += data
                if data.endswith(b""):
                    break
            file_path = os.path.join(LAN_FILES_DIR, new_filename)
            with open(file_path, "wb") as f:
                f.write(file_contents)
        else:
            print(msg)

    client_socket.close()


receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()

while True:
    pass
