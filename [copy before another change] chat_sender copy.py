import socket
import threading

HOST = 'localhost'
PORT = 9994

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []


def client_handler(conn, addr):
    while True:
        try:
            msg = conn.recv(1024).decode('utf-8')

            if msg == 'quit':
                break

            for client in clients:
                if client != conn:
                    client.send(msg.encode('utf-8'))

        except:
            clients.remove(conn)
            break

    conn.close()


def accept_connections():
    while True:
        conn, addr = server.accept()
        clients.append(conn)

        t = threading.Thread(target=client_handler, args=(conn, addr))
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
