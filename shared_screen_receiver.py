# student [view instructor screen]

# from vidstream import StreamingServer
from shared_screen_module import StreamingServer
import threading

stop_server = False


def start_receiver(ip_address, port):
    print(f'ip_address: {ip_address}')
    print(f'port: {port}')

    # server
    receiver = StreamingServer(ip_address, port)

    t = threading.Thread(target=receiver.start_server)
    t.start()

    while not stop_server:
        continue

    # When You Are Done
    receiver.stop_server()


def stop_receiver():
    global stop_server
    stop_server = True


start_receiver("192.168.1.12", 9995)
