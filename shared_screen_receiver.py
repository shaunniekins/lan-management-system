# student [view instructor screen]

from vidstream import StreamingServer
import threading
import socket


def start_receiver(ip_address, port):
    print(f'ip_address: {ip_address}')
    print(f'port: {port}')

    # server
    receiver = StreamingServer(ip_address, port)

    t = threading.Thread(target=receiver.start_server)
    t.start()

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
start_receiver(ip_address, 9995)
