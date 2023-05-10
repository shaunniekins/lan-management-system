import tkinter
from tkinter import ttk
from tkinter import messagebox
import socket

import customtkinter
from utils.register_user_ip_address import check_user_ip_address, close_lan_active

from userInstructor.components.Register import RegisterFrame
from userInstructor.components.RemoteAccess import RemoteAccessFrame
from userInstructor.components.ViewSubject import ViewSubjectFrame
from userInstructor.components.Chat import ChatScreen
from userInstructor.components.Attendance import AttendanceFrame


class InstructorDashboard(customtkinter.CTk):
    def __init__(self, id, first_name, last_name, appearance_mode, user_type):
        super().__init__()

        self.frames = {}

        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.appearance_mode = appearance_mode
        self.user_type = user_type

        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

        check_user_ip_address(self.id, self.user_type, ip_address, 1)

        self.geometry(f"{1200}x{650}")
        self.title("LAN Connect - Instructor Dashboard")

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
            text="Instructor\nDashboard",
            font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(side="top", pady=(30, 30))

        self.sidebar_register = customtkinter.CTkButton(
            master=self.sidebar_container, text="Register Subject", command=lambda: self.sidebar_button_event(self.sidebar_register), state="disabled")
        self.sidebar_register.pack(pady=10)

        self.sidebar_view_subject = customtkinter.CTkButton(
            master=self.sidebar_container, text="View Subject", command=lambda: self.sidebar_button_event(self.sidebar_view_subject))
        self.sidebar_view_subject.pack(pady=10)

        self.sidebar_chat_screen = customtkinter.CTkButton(
            master=self.sidebar_container, text="Chat", command=lambda: self.sidebar_button_event(self.sidebar_chat_screen))
        self.sidebar_chat_screen.pack(pady=10)

        self.sidebar_remote_access = customtkinter.CTkButton(
            master=self.sidebar_container, text="Remote Access", command=lambda: self.sidebar_button_event(self.sidebar_remote_access))
        self.sidebar_remote_access.pack(pady=10)

        self.sidebar_register_id = customtkinter.CTkButton(
            master=self.sidebar_container, text="Register ID", command=self.register_id_event,)
        self.sidebar_register_id.pack(pady=10)
        
        self.sidebar_attendance = customtkinter.CTkButton(
            master=self.sidebar_container, text="Attendance", command=lambda: self.sidebar_button_event(self.sidebar_attendance))
        self.sidebar_attendance.pack(pady=10)        

        # self.logout_btn = customtkinter.CTkButton(
        #     master=self.sidebar_container, fg_color=("red"), text="Logout", command=self.logout_event)
        # self.logout_btn.pack(side="bottom", pady=(0, 10))

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
        self.register_frame = RegisterFrame(self.main_frame, self.id)
        self.view_subject_frame = ViewSubjectFrame(self.main_frame, self.id)
        self.remote_access_frame = RemoteAccessFrame(self.main_frame)
        self.chat_frame = ChatScreen(self.main_frame)
        self.attendance_frame = AttendanceFrame(self.main_frame, self.id)

        self.sidebar_button_event(self.sidebar_register)

        self.appearance_mode_optionemenu.set(self.appearance_mode.capitalize())
        self.scaling_optionemenu.set("100%")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            close_lan_active(self.id, 0)
            self.destroy()

    def register_id_event(self):
        from userInstructor.components.RegisterStudentID import RegisterStudentID

        self.sidebar_register_id.configure(state='disabled')

        window = RegisterStudentID(self.sidebar_register_id)
        window.grab_set()
        # window.withdraw()
        window.protocol("WM_DELETE_WINDOW",
                        lambda: self.on_window_close(window))
        window.mainloop()

    def on_window_close(self, window):
        window.grab_release()
        # window.deiconify()
        # Enable the button when the window is closed
        self.sidebar_register_id.configure(state='normal')
        window.destroy()

    def logout_event(self):
        from login import App

        close_lan_active(self.id, 0)

        login_window = App()
        self.destroy()
        login_window.mainloop()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self, button):
        for btn in [self.sidebar_register, self.sidebar_view_subject, self.sidebar_chat_screen, self.sidebar_remote_access, self.sidebar_attendance]:
            if btn == button:
                btn.configure(state="disabled")
            else:
                btn.configure(state="normal")

        if button == self.sidebar_register:
            self.register_frame.register_frame.pack(
                fill="both", expand=True)
            self.view_subject_frame.view_subject_frame.pack_forget()
            self.chat_frame.chat_frame.pack_forget()
            self.remote_access_frame.remote_access_frame.pack_forget()
            self.attendance_frame.attendance_frame.pack_forget()
            
        elif button == self.sidebar_view_subject:
            self.register_frame.register_frame.pack_forget()
            self.view_subject_frame.view_subject_frame.pack(
                fill="both", expand=True)
            self.chat_frame.chat_frame.pack_forget()
            self.remote_access_frame.remote_access_frame.pack_forget()
            self.attendance_frame.attendance_frame.pack_forget()
            
        elif button == self.sidebar_chat_screen:
            self.register_frame.register_frame.pack_forget()
            self.view_subject_frame.view_subject_frame.pack_forget()
            self.chat_frame.chat_frame.pack(
                fill="both", expand=True)
            self.remote_access_frame.remote_access_frame.pack_forget()
            self.attendance_frame.attendance_frame.pack_forget()
            
        elif button == self.sidebar_remote_access:
            self.register_frame.register_frame.pack_forget()
            self.view_subject_frame.view_subject_frame.pack_forget()
            self.chat_frame.chat_frame.pack_forget()
            self.remote_access_frame.remote_access_frame.pack(
                fill="both", expand=True)
            self.attendance_frame.attendance_frame.pack_forget()
            
        elif button == self.sidebar_attendance:
            self.register_frame.register_frame.pack_forget()
            self.view_subject_frame.view_subject_frame.pack_forget()
            self.chat_frame.chat_frame.pack_forget()
            self.remote_access_frame.remote_access_frame.pack_forget()
            self.attendance_frame.attendance_frame.pack(fill='both', expand=True)
