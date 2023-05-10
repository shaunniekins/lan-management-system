import cv2
from tkinter import ttk
from tkinter import messagebox
import customtkinter
import socket
from vidstream import StreamingServer
import threading


from utils.db_connection import get_database


class ChatScreen:
    def __init__(self, parent_frame):

        super().__init__()

        # self.HOST = 'localhost'
        self.PORT = 9990

        self.parent_frame = parent_frame

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

        db = get_database()
        cursor = db.cursor()
        query = """
            SELECT user_instructor.last_name, user_instructor.first_name, active_user_ip.ip_address
            FROM active_user_ip
            INNER JOIN user_instructor ON active_user_ip.user_id = user_instructor.id
            WHERE user_type='instructor' AND is_active=0
            ORDER BY (user_instructor.last_name) ASC;
        """
        cursor.execute(query)
        result = cursor.fetchall()
        self.instructor_ip_dict = {
            f"{row[0]}, {row[1]}": row[2] for row in result
        }

        self.options = ["-- Select instructor Server --"] + \
            list(self.instructor_ip_dict.keys())

        self.select_server_option = customtkinter.CTkOptionMenu(
            self.content_container, values=self.options, width=200, command=self.set_host_from_instructor_name)
        self.select_server_option.pack(
            side="top", anchor="ne", padx=(0, 30))

        self.textbox = customtkinter.CTkTextbox(
            master=self.content_container, corner_radius=0, font=('Calibri', 15))
        self.textbox.pack(fill="both", expand=True)
        # self.textbox.insert("end", "\n[ Start ]\n\n", 'gray')
        # self.textbox.tag_config('gray', foreground='gray')
        self.textbox.configure(state="disabled")

    def set_host_from_instructor_name(self, selected_option):
        if selected_option != "-- Select instructor Server --":
            self.HOST = self.instructor_ip_dict[selected_option].strip()
            self.receive_thread = threading.Thread(
                target=self.receive_messages)
            self.receive_thread.daemon = True
            self.receive_thread.start()

    def receive_messages(self):
        host = self.HOST

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.HOST, self.PORT))

        while True:
            msg = client_socket.recv(1024).decode('utf-8')

            if not msg:
                break
            self.textbox.configure(state="normal")
            self.textbox.insert("end", "Instructor: ", 'yellow')
            self.textbox.insert("end", f"{msg}\n", 'white')
            self.textbox.tag_config('yellow', foreground='yellow')
            self.textbox.tag_config('white', foreground='white')
            self.textbox.configure(state="disabled")

        client_socket.close()
