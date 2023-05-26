import cv2
from tkinter import ttk
from tkinter import messagebox
import customtkinter
import socket
from vidstream import StreamingServer
import threading
# from remote_control import remote
import subprocess
import time
import datetime
import os


from utils.db_connection import get_database
from utils.register_user_ip_address import check_user_ip_address_student


class ChatScreen:
    def __init__(self, parent_frame, id, full_name, user_type, ip_address, appearance_mode):
        super().__init__()

        self.parent_frame = parent_frame
        self.id = id
        self.full_name = full_name
        self.user_type = user_type
        self.ip_address = ip_address
        self.appearance_mode = appearance_mode


        self.HOST = None
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
        
        # self.set_host_and_execute_remote_main()

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
            
    # def set_host_and_execute_remote_main(self):
    #     if self.HOST is not None:
    #         host = f'http://{self.HOST}:5000'
    #         key = str(self.id)

    #         time.sleep(15)  # Wait for 15 seconds   
    #         self.execute_remote_main(host, key)
    
    # # # new set_host_and_execute_remote_main function to use
    def set_host_and_execute_remote_main(self, host=None):
        if host is None:
            host = self.HOST

        if host is not None:
            host = f'http://{host}:5000'
            key = str(self.id)

            time.sleep(15)  # Wait for 15 seconds

            # Execute remote.main in a separate thread
            remote_thread = threading.Thread(
                target=self.execute_remote_main, args=(host, key)
            )
            remote_thread.start()
            
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
            print('selected_option: ', selected_option)
            self.HOST = self.new_instructor_ip_dict[selected_option].strip()

            if self.receive_thread and self.receive_thread.is_alive():
                # Thread is already running, just update the HOST
                self.receive_messages_stop = False
                self.message_entry.configure(state="normal")
            else:
                # Thread is not running, start a new one
                self.receive_messages_stop = False
                self.receive_thread = threading.Thread(
                    target=self.receive_messages)
                self.receive_thread.daemon = True
                self.receive_thread.start()
                print('host: ', self.HOST)

            # self.set_host_and_execute_remote_main()

            connection_ip_address = self.HOST
            check_user_ip_address_student(self.id, self.user_type, self.ip_address, connection_ip_address, 1)
        else:
            if self.receive_thread and self.receive_thread.is_alive():
                # Stop the thread and clear the textbox
                self.receive_messages_stop = True
                self.textbox.configure(state="normal")
                self.textbox.delete('1.0', 'end')
                self.textbox.configure(state="disabled")

    # def execute_remote_main(self, host, key):
    #     remote.main(host, key)

    def messages(self, event=None):
        msg = self.message_entry.get()
        msg_to_send = f'<<<::{self.full_name}::>>>{msg}'
        

        if msg != '':
            self.textbox.configure(state="normal")
            self.textbox.insert("end", "You: ", 'green')
            self.textbox.insert("end", f"{msg}\n", 'white')
            self.textbox.tag_config('green', foreground='green')
            
            if self.appearance_mode == 'Dark':
                self.textbox.tag_config('white', foreground='white')
            elif self.appearance_mode == 'Light':
                self.textbox.tag_config('white', foreground='black')
                
            self.textbox.configure(state="disabled")


            self.client_socket.send(msg_to_send.encode('utf-8'))
            if msg == "quit":
                self.receive_messages_stop = True  # Stop receiving messages

            self.message_entry.delete(0, "end")


    def receive_messages(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.HOST, self.PORT))
        
        LAN_FILES_DIR = os.path.expanduser("~/Documents/LAN_Files")
        if not os.path.exists(LAN_FILES_DIR):
            os.makedirs(LAN_FILES_DIR)

        while not self.receive_messages_stop:
            msg = self.client_socket.recv(1024).decode('utf-8')

            if not msg:
                if msg.startswith("<FILE>"):
                    filename_start = msg.find("<FILE>") + len("<FILE>")
                    filename_end = msg.find("<FILE>", filename_start)
                    filename = msg[filename_start:filename_end]

                    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    new_filename = f"{current_time}_{os.path.basename(filename)}"
                    file_contents = b""
                    while True:
                        data = self.client_socket.recv(1024)
                        if not data:
                            break
                        file_contents += data
                        if data.endswith(b""):
                            break
                    file_path = os.path.join(LAN_FILES_DIR, new_filename)
                    with open(file_path, "wb") as f:
                        f.write(file_contents)
                break
            else:
                if msg != '':
                    self.textbox.configure(state="normal")
                    if '<<<::' in msg and '::>>>' in msg:
                        name_start = msg.index('<<<::') + 5
                        name_end = msg.index('::>>>')
                        name = msg[name_start:name_end]
                        content_start = name_end + 5
                        content = msg[content_start:]
                        self.textbox.insert("end", f"{name}: ", 'yellow')
                        self.textbox.insert("end", f"{content}\n", 'white')
                    else:
                        self.textbox.insert("end", "Instructor: ", 'violet')
                        self.textbox.insert("end", f"{msg}\n", 'white')
                    self.textbox.tag_config('violet', foreground='violet')
                    self.textbox.tag_config('yellow', foreground='yellow')
                    
                    if self.appearance_mode == 'Dark':
                        self.textbox.tag_config('white', foreground='white')
                    elif self.appearance_mode == 'Light':
                        self.textbox.tag_config('white', foreground='black')
                        
                    self.textbox.configure(state="disabled")

        self.client_socket.close()