import threading
from vidstream import ScreenShareClient


# client
sender = ScreenShareClient("192.168.1.11", 9999)

t = threading.Thread(target=sender.start_stream())
t.start()

while input("") != 'STOP':
    continue

sender.stop_stream()
