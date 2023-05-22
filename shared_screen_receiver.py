from vidstream import StreamingServer
import threading
import socket

def start_receiver(ip_address, port):
    receiver = StreamingServer(ip_address, port)

    while True:
        try:
            receiver.start_server()
        except OSError as e:
            if e.errno == 98:
                receiver.release_socket()
            else:
                raise e
        else:
            break

# Start the receiver immediately
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
start_receiver(ip_address, 9996)