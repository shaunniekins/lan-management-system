import cv2
from tkinter import ttk
from tkinter import messagebox
import customtkinter
import socket
from vidstream import StreamingServer
import threading
# from remote_control import remote
import subprocess


from utils.db_connection import get_database
from utils.register_user_ip_address import check_user_ip_address_student


class ChatScreen:
    def __init__(self, parent_frame, id, full_name, user_type, ip_address):
        super().__init__()

        self.parent_frame = parent_frame
        self.id = id
        self.full_name = full_name
        self.user_type = user_type
        self.ip_address = ip_address

        # self.HOST = 'localhost'
        self.PORT = 9995
       
        self.receive_thread = None
        self.receive_messages_flag = False
        
        self.instructor_ip_dict = {}


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
            WHERE user_type='instructor' AND is_active=1
            ORDER BY (user_instructor.last_name) ASC;
        """
        cursor.execute(query)
        result = cursor.fetchall()
        self.instructor_ip_dict = {f"{row[0]}, {row[1]}".strip(): row[2] for row in result}


        self.options = ["-- Select instructor Server --"] + \
            list(self.instructor_ip_dict.keys())

        self.select_server_option = customtkinter.CTkOptionMenu(
            self.content_container, values=self.options, width=200, command=self.set_host_from_instructor_name)
        self.select_server_option.pack(
            side="top", anchor="ne", padx=(0, 30))

        self.textbox = customtkinter.CTkTextbox(
            master=self.content_container, corner_radius=0, font=('Calibri', 15))
        self.textbox.pack(fill="both", expand=True)
        self.textbox.configure(state="disabled")


        db.close()

        self.timer_interval = 5000  # 5 seconds
        self.check_for_new_data()


        # chat message area
        self.send_msg_container = customtkinter.CTkFrame(
            master=self.content_container, corner_radius=0)
        self.send_msg_container.pack(
            side="bottom", anchor="s", fill="x", expand=False)

        # create main entry and button
        self.message_entry = customtkinter.CTkEntry(
            master=self.send_msg_container, placeholder_text="Enter Message", width=600, height=40, font=("Helvetica", 15))
        self.message_entry.grid(row=3, column=0, columnspan=5, padx=(
            20, 0), pady=15, sticky="nsew")
        # self.message_entry.bind(
        #     "<Shift-Return>", lambda event: self.message_entry.insert("insert", "\n"))
        self.message_entry.bind("<Return>", lambda event: self.messages())

        self.send_btn = customtkinter.CTkButton(
            master=self.send_msg_container, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Send", command=self.messages)
        self.send_btn.grid(row=3, column=6, padx=20, pady=15,  sticky="nsew")

        self.send_msg_container.rowconfigure(3, weight=3)
        self.send_msg_container.columnconfigure(0, weight=1)
        self.send_msg_container.columnconfigure(5, weight=0)
        self.send_msg_container.columnconfigure(6, weight=0)
        
        # if self.select_server_option.get() == "-- Select instructor Server --":
        #     self.message_entry.configure(state="disabled")
        # else:
        #     self.message_entry.configure(state="normal")
            
            
            
    def check_for_new_data(self):
        # print("check for update.............")
        db = get_database()
        cursor = db.cursor()
        query = """
            SELECT user_instructor.last_name, user_instructor.first_name, active_user_ip.ip_address
            FROM active_user_ip
            INNER JOIN user_instructor ON active_user_ip.user_id = user_instructor.id
            WHERE user_type='instructor' AND is_active=1
            ORDER BY (user_instructor.last_name) ASC;
        """
        cursor.execute(query)
        result = cursor.fetchall()
        
        self.new_instructor_ip_dict = {
            f"{row[0]}, {row[1]}": row[2] for row in result
        }
        
        # self.select_server_option['menu'].delete(0, 'end')
        
        self.new_options = ["-- Select instructor Server --"] + \
            list(self.new_instructor_ip_dict.keys())
            
        self.select_server_option.configure(values=self.new_options)
            
        db.close()
        self.chat_frame.after(self.timer_interval, self.check_for_new_data)


    def set_host_from_instructor_name(self, selected_option):
        if selected_option != "-- Select instructor Server --":
            print('selected_option: ',selected_option)
            
            self.HOST = self.new_instructor_ip_dict[selected_option].strip()
            if self.receive_thread and self.receive_thread.is_alive():
                # Thread is already running, just update the HOST
                self.receive_messages_stop = False
                self.message_entry.configure(state="normal")
                print('host: ', self.HOST)
            else:
                # Thread is not running, start a new one
                self.receive_messages_stop = False
                self.receive_thread = threading.Thread(
                    target=self.receive_messages)
                self.receive_thread.daemon = True
                self.receive_thread.start()
                print('host: ', self.HOST)

            connection_ip_address = self.HOST
            check_user_ip_address_student(self.id, self.user_type, self.ip_address, connection_ip_address, 1)
            print("self.id: ", self.id)
            print("self.user_type: ", self.user_type)
            print("self.ip_address ",self.ip_address)
            print("self.HOST: ", self.HOST)
            

            host = (f'{self.HOST}:5000')
            key = self.id

            # remote.main(host, key)
        else:
            if self.receive_thread and self.receive_thread.is_alive():
                # Stop the thread and clear the textbox
                self.receive_messages_stop = True
                self.textbox.configure(state="normal")
                self.textbox.delete('1.0', 'end')
                self.textbox.configure(state="disabled")

    def messages(self, event=None):
        msg = self.message_entry.get()
        msg_to_send = f'<<<::{self.full_name}::>>>{msg}'
        

        if msg != '':
            self.textbox.configure(state="normal")
            self.textbox.insert("end", "You: ", 'green')
            self.textbox.insert("end", f"{msg}\n", 'white')
            self.textbox.tag_config('green', foreground='green')
            self.textbox.tag_config('white', foreground='white')
            self.textbox.configure(state="disabled")

            self.client_socket.send(msg_to_send.encode('utf-8'))
            if msg == "quit":
                self.receive_messages_stop = True  # Stop receiving messages

            self.message_entry.delete(0, "end")


    def receive_messages(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.HOST, self.PORT))

        while not self.receive_messages_stop:
            msg = self.client_socket.recv(1024).decode('utf-8')

            if not msg:
                break
            self.textbox.configure(state="normal")
            self.textbox.insert("end", "Instructor: ", 'yellow')
            self.textbox.insert("end", f"{msg}\n", 'white')
            self.textbox.tag_config('yellow', foreground='yellow')
            self.textbox.tag_config('white', foreground='white')
            self.textbox.configure(state="disabled")

        self.client_socket.close()
        

