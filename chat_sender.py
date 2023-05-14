import socket
import threading

hostname = socket.gethostname()
HOST = socket.gethostbyname(hostname)
PORT = 9995

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []

def client_handler(conn, addr, clients):
    while True:
        try:
            msg = conn.recv(1024).decode('utf-8')

            if not msg:
                break
            else:
                print("message:", msg)  # Print received message

            for client in clients.copy():
                if client != conn:
                    try:
                        client.send(msg.encode('utf-8'))
                    except BrokenPipeError:
                        clients.remove(client)
                        print("Client disconnected")
        except:
            break

    conn.close()
    if conn in clients:
        clients.remove(conn)
    print("Client disconnected:", addr)

def accept_connections():
    while True:
        conn, addr = server.accept()
        clients.append(conn)

        t = threading.Thread(target=client_handler, args=(conn, addr, clients))
        t.daemon = True
        t.start()

        print("Client connected:", addr)

def send_messages(clients):
    while True:
        message = input("Type your message: ")

        if message == 'quit':
            break

        for client in clients.copy():
            try:
                client.send(message.encode('utf-8'))
            except BrokenPipeError:
                clients.remove(client)
                print("Client disconnected")

    for client in clients:
        client.close()

accept_thread = threading.Thread(target=accept_connections)
accept_thread.daemon = True
accept_thread.start()

send_thread = threading.Thread(target=send_messages, args=(clients,))
send_thread.daemon = True
send_thread.start()

accept_thread.join()
send_thread.join()

        # if msg.startswith("<FILE>"):
        #     # The message contains file data
        #     filename_start = msg.find("<FILE>") + len("<FILE>")
        #     filename_end = msg.find("<FILE>", filename_start)
        #     filename = msg[filename_start:filename_end]

        #     current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        #     new_filename = f"{current_time}_{os.path.basename(filename)}"
        #     file_contents = b""
        #     while True:
        #         data = client_socket.recv(1024)
        #         if not data:
        #             break
        #         file_contents += data
        #         if data.endswith(b""):
        #             break
        #     file_path = os.path.join(LAN_FILES_DIR, new_filename)
        #     with open(file_path, "wb") as f:
        #         f.write(file_contents)
        # else:
        #     print(msg)