import tkinter
from tkinter import ttk
from tkinter import messagebox
import socket

import customtkinter
from utils.register_user_ip_address import check_user_ip_address_student
from utils.register_user_ip_address import close_lan_active_student


from userStudent.components.AddSubject import AddSubjectFrame
from userStudent.components.Chat import ChatScreen

from utils.db_connection import get_database

import datetime

import subprocess
import os
import signal

class StudentDashboard(customtkinter.CTk):
    def __init__(self, id, first_name, last_name, appearance_mode, user_type):
        super().__init__()
        
        self.id = id
        self.mark_attendance()
        

        self.frames = {}

        self.frames = {}

        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.appearance_mode = appearance_mode
        self.user_type = user_type
        self.full_name = f'{self.last_name}, {self.first_name}'

        hostname = socket.gethostname()
        self.ip_address = socket.gethostbyname(hostname)

        check_user_ip_address_student(self.id, self.user_type, self.ip_address, '', 1)

        self.geometry(f"{1200}x{650}")
        self.title("LAN Connect - Student Dashboard")

        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True)

        self.sidebar_frame = customtkinter.CTkFrame(
            self.main_frame, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.pack_propagate(0)

        self.topbar_frame = customtkinter.CTkFrame(
            self.main_frame, corner_radius=0)
        self.topbar_frame.pack(side="top", fill="x", padx=25)
        self.topbar_frame.pack_propagate(0)
        self.topbar_frame.configure(height=40)

        self.topbar_container = customtkinter.CTkFrame(self.topbar_frame)
        self.topbar_container.pack(side="right", fill="both", expand=True)

        self.logout_btn = customtkinter.CTkButton(
            master=self.topbar_container,
            fg_color="red",
            text="⏏️",
            command=self.logout_event,
            compound="left",
            width=20,  # set the width to 50 pixels
            height=20  # set the height to 20 pixels
        )
        self.logout_btn.pack(side="right", padx=(10, 0))

        self.greetings_label = customtkinter.CTkLabel(
            master=self.topbar_container,
            text=f'Hi, {self.first_name} {self.last_name}',
            font=customtkinter.CTkFont(size=15, weight="normal"))
        self.greetings_label.pack(side="right")

        self.sidebar_container = customtkinter.CTkFrame(self.sidebar_frame)
        self.sidebar_container.pack(fill="both", expand=True)

        self.logo_label = customtkinter.CTkLabel(
            master=self.sidebar_container,
            text="Student\nDashboard",
            font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(side="top", pady=(30, 30))

        self.sidebar_add_subject = customtkinter.CTkButton(
            master=self.sidebar_container, text="Register Subject", command=lambda: self.sidebar_button_event(self.sidebar_add_subject))
        self.sidebar_add_subject.pack(pady=10)

        # self.sidebar_add_subject = customtkinter.CTkButton(
        #     master=self.sidebar_container, text="Add Subject", command=lambda: self.sidebar_button_event(self.sidebar_add_subject))
        # self.sidebar_add_subject.pack(pady=10)

        self.sidebar_chat_screen = customtkinter.CTkButton(
            master=self.sidebar_container, text="Chat", command=lambda: self.sidebar_button_event(self.sidebar_chat_screen))
        self.sidebar_chat_screen.pack(pady=10)

        self.sidebar_view_shared_screen = customtkinter.CTkButton(
            master=self.sidebar_container, text="View Shared Screen", command=self.view_shared_screen_event)
        self.sidebar_view_shared_screen.pack(pady=10)

        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_container, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.pack(side="bottom", pady=(0, 30))

        self.scaling_label = customtkinter.CTkLabel(
            master=self.sidebar_container, text="UI Scaling:", anchor="w")
        self.scaling_label.pack(side="bottom", pady=(0, 10))

        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_container, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.pack(side="bottom", pady=(0, 10))
        self.appearance_mode_label = customtkinter.CTkLabel(
            master=self.sidebar_container, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.pack(side="bottom", pady=(0, 10))

        self.sidebar_container.pack_propagate(0)
        self.sidebar_container.pack(fill="both", expand=True)

        # frames
        self.add_subject_frame = AddSubjectFrame(self.main_frame, self.id)
        self.chat_frame = ChatScreen(self.main_frame, self.id, self.full_name, self.user_type, self.ip_address)

        self.sidebar_button_event(self.sidebar_add_subject)

        self.appearance_mode_optionemenu.set(self.appearance_mode.capitalize())
        self.scaling_optionemenu.set("100%")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.receiver_process = None # Initialize sender_process as None

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            # close_lan_active(self.id, 0)
            close_lan_active_student(self.id, 0, ' ')
            
            
            self.on_close()
            self.destroy()
            
    def on_close(self):
        # WIN_LIN
        
        # subprocess.Popen(["pkill", "-9", "-f", "shared_screen_receiver.py"])
        subprocess.call('taskkill /F /IM python.exe /T /FI "WINDOWTITLE eq shared_screen_receiver.py"', shell=True)
        
        # subprocess.Popen(["pkill", "-9", "-f", "app.py"])
        subprocess.call('taskkill /F /IM python.exe /T /FI "WINDOWTITLE eq app.py"', shell=True)
        
        # subprocess.Popen(["pkill", "-9", "-f", "remote.py"])
        subprocess.call('taskkill /F /IM python.exe /T /FI "WINDOWTITLE eq remote.py"', shell=True)

    def view_shared_screen_event(self):
        if self.receiver_process is not None:
            # subprocess.Popen(["pkill", "-9", "-f", "shared_screen_receiver.py"])
            subprocess.call('taskkill /F /IM python.exe /T /FI "WINDOWTITLE eq shared_screen_receiver.py"', shell=True)
            
            self.receiver_process = None
            self.sidebar_view_shared_screen.configure(fg_color="green", text="View Screen") # Change button text to "Share Screen"
        else:
            # subprocess.Popen(["pkill", "-9", "-f", "shared_screen_receiver.py"])
            subprocess.call('taskkill /F /IM python.exe /T /FI "WINDOWTITLE eq shared_screen_receiver.py"', shell=True)
            
            # self.receiver_process = subprocess.Popen("python shared_screen_receiver.py", shell=True, preexec_fn=os.setpgrp) # Start the sender_process in a new process group
            self.receiver_process = subprocess.Popen("python shared_screen_receiver.py", shell=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
            
            self.sidebar_view_shared_screen.configure(fg_color="red", text="Stop View Screen") # Change button text to "Stop Share Screen"
   
    # def view_shared_screen_event(self):
    #     subprocess.Popen(["pkill", "-9", "-f", "shared_screen_receiver.py"])
    #     # subprocess.call('taskkill /F /IM python.exe /T /FI "WINDOWTITLE eq shared_screen_receiver.py"', shell=True)
        
    #     self.receiver_process = subprocess.Popen("python shared_screen_receiver.py", shell=True, preexec_fn=os.setpgrp) # Start the sender_process in a new process group
    #     # self.receiver_process = subprocess.Popen("python shared_screen_receiver.py", shell=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
  
  
    def on_window_close(self, window):
        # Enable the button when the window is closed
        self.sidebar_view_shared_screen.configure(state='normal')
        
        # subprocess.Popen(["pkill", "-9", "-f", "shared_screen_receiver.py"])
        subprocess.call('taskkill /F /IM python.exe /T /FI "WINDOWTITLE eq shared_screen_receiver.py"', shell=True)
        
        # subprocess.Popen(["pkill", "-9", "-f", "app.py"])
        subprocess.call('taskkill /F /IM python.exe /T /FI "WINDOWTITLE eq app.py"', shell=True)
        
        # subprocess.Popen(["pkill", "-9", "-f", "remote.py"])
        subprocess.call('taskkill /F /IM python.exe /T /FI "WINDOWTITLE eq remote.py"', shell=True)
        window.destroy()

    def logout_event(self):
        from login import App

        # close_lan_active(self.id, 0)
        close_lan_active_student(self.id, 0, ' ')
        

        login_window = App()
        
        # subprocess.Popen(["pkill", "-9", "-f", "shared_screen_receiver.py"])
        subprocess.call('taskkill /F /IM python.exe /T /FI "WINDOWTITLE eq shared_screen_receiver.py"', shell=True)
        
        # subprocess.Popen(["pkill", "-9", "-f", "app.py"])
        subprocess.call('taskkill /F /IM python.exe /T /FI "WINDOWTITLE eq app.py"', shell=True)
        
        # subprocess.Popen(["pkill", "-9", "-f", "remote.py"])
        subprocess.call('taskkill /F /IM python.exe /T /FI "WINDOWTITLE eq remote.py"', shell=True)
        
        self.on_close()
        self.destroy()
        login_window.mainloop()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self, button):
        for btn in [self.sidebar_add_subject, self.sidebar_chat_screen]:
            if btn == button:
                btn.configure(state="disabled")
            else:
                btn.configure(state="normal")

        if button == self.sidebar_add_subject:
            self.add_subject_frame.add_subject_frame.pack(
                fill="both", expand=True)
            self.chat_frame.chat_frame.pack_forget()
        elif button == self.sidebar_chat_screen:
            self.add_subject_frame.add_subject_frame.pack_forget()
            self.chat_frame.chat_frame.pack(
                fill="both", expand=True)

    def mark_attendance(self):
        # get current date and time
        current_date_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # check if attendance has already been marked for this student on this date
        db = get_database()
        cursor = db.cursor()
        query = "SELECT * FROM student_attendance WHERE student_number = %s AND date = %s"
        values = (self.id, current_date_time.split()[0])
        cursor.execute(query, values)
        # cursor.execute(query, values)
        result = cursor.fetchone()  # Fetch the result even if you don't use it
        attendance_data = cursor.fetchone()

        if not result:
            query = "INSERT INTO student_attendance (student_number, date, time) VALUES (%s, %s, %s)"
            values = (self.id, current_date_time.split()[0], current_date_time.split()[1])
            cursor.execute(query, values)
            db.commit()
            db.close()
