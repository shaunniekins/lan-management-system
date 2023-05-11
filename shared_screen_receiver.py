from vidstream import StreamingServer
import threadingz
import socket


def start_receiver(ip_address, port):
    print(f'ip_address: {ip_address}')
    print(f'port: {port}')

    receiver = StreamingServer(ip_address, port)

    while True:
        try:
            receiver.start_server()
        except OSError as e:
            if e.errno == 98:
                print(f"Port {port} already in use. Releasing the socket...")
                receiver.release_socket()
            else:
                raise e
        else:
            break


hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
start_receiver(ip_address, 9999)
