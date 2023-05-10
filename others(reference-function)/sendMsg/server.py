import tkinter as tk
import socket
import threading

from client import handle_client

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


class ServerGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Server GUI")
        self.master.geometry("300x200")
        self.create_widgets()

    def create_widgets(self):
        self.start_button = tk.Button(
            self.master, text="Start Server", command=self.start_server)
        self.start_button.pack(pady=20)

        self.stop_button = tk.Button(
            self.master, text="Stop Server", command=self.stop_server, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.status_label = tk.Label(self.master, text="")
        self.status_label.pack()

    def start_server(self):
        self.server_thread = threading.Thread(target=self.server_start)
        self.server_thread.start()
        self.status_label.configure(text="Server is running...")
        self.start_button.configure(state=tk.DISABLED)
        self.stop_button.configure(state=tk.NORMAL)

    def server_start(self):
        server.listen()
        print(f"[LISTENING] Server is listening on {SERVER}")
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

    def stop_server(self):
        self.server_thread._stop()
        self.status_label.configure(text="Server stopped.")
        self.start_button.configure(state=tk.NORMAL)
        self.stop_button.configure(state=tk.DISABLED)


root = tk.Tk()
app = ServerGUI(master=root)
app.mainloop()
