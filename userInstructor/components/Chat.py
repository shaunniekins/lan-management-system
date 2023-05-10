import cv2
from tkinter import ttk
from tkinter import messagebox
import customtkinter
import socket
from vidstream import StreamingServer
import threading
import tkinter.filedialog
import os


from utils.db_connection import get_database


class ChatScreen:
    def __init__(self, parent_frame):

        super().__init__()

        hostname = socket.gethostname()
        self.HOST = socket.gethostbyname(hostname)
        self.PORT = 9997

        self.parent_frame = parent_frame

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.HOST, self.PORT))
        self.server.listen()

        self.clients = []

        # Start accepting connections in the background
        accept_thread = threading.Thread(target=self.accept_connections)
        accept_thread.daemon = True
        accept_thread.start()

        self.chat_frame = customtkinter.CTkFrame(self.parent_frame)
        self.chat_frame.pack(fill="both", expand=True)

        # container
        self.chat_container = customtkinter.CTkFrame(
            self.chat_frame, corner_radius=0)
        self.chat_container.pack(fill="both", expand=True)
        self.chat_container.pack_propagate(0)
        self.chat_container.configure(height=950)

        self.content_container = customtkinter.CTkFrame(
            self.chat_container, corner_radius=0)
        self.content_container.pack(fill="both", expand=True)

        self.textbox = customtkinter.CTkTextbox(
            master=self.content_container, corner_radius=0, font=('Calibri', 15))
        self.textbox.pack(fill="both", expand=True)
        self.textbox.configure(state="disabled")

        # chat message area
        self.send_msg_container = customtkinter.CTkFrame(
            master=self.content_container, corner_radius=0)
        self.send_msg_container.pack(
            side="bottom", anchor="s", fill="x", expand=False)

        # create main entry and button
        self.message_entry = customtkinter.CTkEntry(
            master=self.send_msg_container, placeholder_text="Enter Message", width=600, height=40, font=("Helvetica", 15))
        self.message_entry.grid(row=3, column=0, columnspan=4, padx=(
            20, 0), pady=15, sticky="nsew")
        # self.message_entry.bind(
        #     "<Shift-Return>", lambda event: self.message_entry.insert("insert", "\n"))
        self.message_entry.bind("<Return>", lambda event: self.messages())

        self.send_btn = customtkinter.CTkButton(
            master=self.send_msg_container, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Send", command=self.messages)
        self.send_btn.grid(row=3, column=5, padx=(
            20, 10), pady=15,  sticky="nsew")

        self.send_file_btn = customtkinter.CTkButton(
            master=self.send_msg_container, fg_color="green", border_width=2, text_color=("gray10", "#DCE4EE"), text="Send File", command=self.send_file)
        self.send_file_btn.grid(row=3, column=6, padx=(
            10, 20), pady=15,  sticky="nsew")

        self.send_msg_container.rowconfigure(3, weight=3)
        self.send_msg_container.columnconfigure(0, weight=1)
        self.send_msg_container.columnconfigure(5, weight=0)
        self.send_msg_container.columnconfigure(6, weight=0)

    def accept_connections(self):
        while True:
            conn, addr = self.server.accept()
            self.clients.append(conn)

            t = threading.Thread(target=self.client_handler,
                                 args=(conn, addr, self.clients))
            t.daemon = True
            t.start()

            print("Client connected:", addr)

    def messages(self, event=None):
        msg = self.message_entry.get()

        if msg != '':
            self.textbox.configure(state="normal")
            self.textbox.insert("end", "You: ", 'green')
            self.textbox.insert("end", f"{msg}\n", 'white')
            self.textbox.tag_config('green', foreground='green')
            self.textbox.tag_config('white', foreground='white')
            self.textbox.configure(state="disabled")

            send_thread = threading.Thread(
                target=self.send_messages, args=(self.clients, msg))
            send_thread.daemon = True
            send_thread.start()

            self.message_entry.delete(0, "end")

    @staticmethod
    def client_handler(conn, addr, clients):
        while True:
            try:
                msg = conn.recv(1024).decode('utf-8')

                if not msg:
                    break

                if msg == 'quit':
                    break

                for client in clients.copy():
                    if client != conn:
                        try:
                            if client.fileno() != -1:
                                client.send(msg.encode('utf-8'))
                            else:
                                clients.remove(client)
                                print("Client disconnected")
                        except BrokenPipeError:
                            clients.remove(client)
                            print("Client disconnected")
            except Exception as e:
                print(f"Error receiving message from client {addr}: {e}")
                break

        conn.close()
        if conn in clients:
            clients.remove(conn)
        print("Client disconnected:", addr)

    def send_messages(self, clients, msg):
        for client in clients.copy():
            try:
                client.send(msg.encode('utf-8'))
            except:
                clients.remove(client)
                print("Client disconnected")

        # Start a new thread to handle the updated clients list
        update_thread = threading.Thread(
            target=self.client_handler, args=(None, None, clients))
        update_thread.daemon = True
        update_thread.start()

    def send_file(self):
        FILE_MARKER = "<FILE>"

        filename = tkinter.filedialog.askopenfilename()
        file_size = os.path.getsize(filename)
        if filename:
            with open(filename, 'rb') as f:
                file_contents = f.read()

            header = f"{FILE_MARKER}{filename}:{file_size}"
            self.client_socket.send(header.encode())
            self.client_socket.send(file_contents)

            self.textbox.configure(state="normal")
            filename_only = os.path.basename(filename)
            self.textbox.insert("end", f"[You sent {filename_only}]\n", 'cyan')
            self.textbox.tag_config('cyan', foreground='cyan')
            self.textbox.configure(state="disabled")

            send_thread = threading.Thread(
                target=self.send_messages, args=(self.clients, header))
            send_thread.daemon = True
            send_thread.start()


