import tkinter as tk
import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

stop_event = threading.Event()
server_running = False


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected and not stop_event.is_set():
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))

    conn.close()
    print(f"[CONNECTION CLOSED] {addr}")


def start_server():
    global server_running
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    server_running = True
    while server_running:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


def start_button_clicked():
    global server_running
    server_running = True
    t = threading.Thread(target=start_server)
    t.start()
    status_label.configure(text="Server is running...")


def stop_server():
    global server_running
    global stop_event
    server_running = False
    stop_event.set()
    print("[STOPPING] Server is stopping...")


root = tk.Tk()
root.title("Server GUI")
root.geometry("300x200")

start_button = tk.Button(root, text="Start Server",
                         command=start_button_clicked)
start_button.pack(pady=20)

stop_button = tk.Button(root, text="Stop Server",
                        command=stop_server, state="disabled")
stop_button.pack(pady=10)

status_label = tk.Label(root, text="")
status_label.pack()


def check_status():
    global server_running
    if server_running:
        start_button.configure(state="disabled")
        stop_button.configure(state="normal")
    else:
        start_button.configure(state="normal")
        stop_button.configure(state="disabled")
    root.after(100, check_status)


root.after(100, check_status)
root.mainloop()
