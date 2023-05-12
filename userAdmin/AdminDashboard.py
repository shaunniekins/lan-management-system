import tkinter
from tkinter import ttk
from tkinter import messagebox
import socket
import time

import customtkinter
from utils.register_user_ip_address import check_user_ip_address, close_lan_active

from userAdmin.components.CreateAccount import CreateAccountFrame
from userAdmin.components.AddItems import AddItemsFrame
# from userAdmin.components.ViewLabServer import ViewLabServerFrame
from userAdmin.components.RemoteAccess import RemoteAccessFrame


from utils.db_connection import get_database


class AdminDashboard(customtkinter.CTk):
    def __init__(self, id, first_name, last_name, appearance_mode, user_type):
        super().__init__()

        self.frames = {}  # Define frames attribute

        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.appearance_mode = appearance_mode
        self.user_type = user_type

        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

        check_user_ip_address(self.id, self.user_type, ip_address, 1)

        # configure window
        self.geometry(f"{1200}x{650}")
        self.title("LAN Connect - Admin Dashboard")

        # create a frame to hold the sidebar and the scrollable frame
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True)

       # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(
            self.main_frame, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y")
        # allow the frame to adjust its size based on contents
        self.sidebar_frame.pack_propagate(0)

       # create topbar frame for log-out and user greetings
        self.topbar_frame = customtkinter.CTkFrame(
            self.main_frame, corner_radius=0)
        self.topbar_frame.pack(side="top", fill="x", padx=25)
        self.topbar_frame.pack_propagate(0)
        self.topbar_frame.configure(height=100)

        self.topbar_container = customtkinter.CTkFrame(self.topbar_frame)
        self.topbar_container.pack(side="right", fill="both", expand=True)

        self.logout_logo_container = customtkinter.CTkFrame(self.topbar_container)
        self.logout_logo_container.grid(row=0, column=6, sticky='ne', padx=10, pady=10)
    


        self.logout_btn = customtkinter.CTkButton(
            master=self.logout_logo_container,
            fg_color="red",
            text="⏏️",
            command=self.logout_event,
            compound="right",
            width=20,  # set the width to 50 pixels
            height=20  # set the height to 20 pixels
        )
        self.logout_btn.grid(row=0, column=1)

        self.logo_label = customtkinter.CTkLabel(
            master=self.logout_logo_container,
            text=f'Hi, {self.first_name} {self.last_name}',
            font=customtkinter.CTkFont(size=15, weight="normal"))
        self.logo_label.grid(row=0, column=0, padx=(1500,10))

        db = get_database()
        cursor = db.cursor()        
        query = "SELECT user_id, ip_address FROM `active_user_ip` WHERE user_type='instructor' AND is_active=1;"
        cursor.execute(query)
        results = cursor.fetchall()
        self.text = "Online servers:\n"
        # for result in results:
        #     user_id, ip_address = result
        #     self.text += f"- User {user_id}: {ip_address}\n"
            
        idCursor = db.cursor()        
        idQuery = "SELECT user_instructor.id, CONCAT(user_instructor.last_name, ', ', user_instructor.first_name) AS Name FROM user_instructor INNER JOIN active_user_ip ON active_user_ip.user_id = user_instructor.id;"
        idCursor.execute(idQuery)
        idResults = idCursor.fetchall()
        
              
        for result in results:
            user_id, ip_address = result
            for idResult in idResults:
                id, name = idResult
                if id == user_id:
                    self.text += f"{name}: {ip_address}\n"
                    break


        self.online_servers_lbl = customtkinter.CTkLabel(
            master=self.topbar_container,
            text=self.text,
            font=customtkinter.CTkFont(size=12, weight="normal"))
        self.online_servers_lbl.grid(row=1, column=6, padx=(1500,10), pady=10)


        # self.logout_logo_container.grid_rowconfigure(0, weight=1)
        self.logout_logo_container.grid_columnconfigure(0, weight=0)
        
        self.online_servers_lbl.grid_columnconfigure(0, weight=0)
        
        


        # create a container frame inside the sidebar frame
        self.sidebar_container = customtkinter.CTkFrame(self.sidebar_frame)
        self.sidebar_container.pack(fill="both", expand=True)

        self.logo_label = customtkinter.CTkLabel(
            master=self.sidebar_container, text="Admin Dashboard", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(side="top", pady=(30, 30))

        self.sidebar_register_instructor = customtkinter.CTkButton(
            master=self.sidebar_container, text="Create Account", command=lambda: self.sidebar_button_event(self.sidebar_register_instructor), state="disabled")
        self.sidebar_register_instructor.pack(pady=(0, 10))

        self.sidebar_add_items = customtkinter.CTkButton(
            master=self.sidebar_container, text="Add Items", command=lambda: self.sidebar_button_event(self.sidebar_add_items))
        self.sidebar_add_items.pack(pady=10)

        # self.sidebar_view_lab_server = customtkinter.CTkButton(
        #     master=self.sidebar_container, text="View Lab Servers", command=lambda: self.sidebar_button_event(self.sidebar_view_lab_server))
        # self.sidebar_view_lab_server.pack(pady=10)

        self.sidebar_remote_access = customtkinter.CTkButton(
            master=self.sidebar_container, text="Remote Access", command=lambda: self.sidebar_button_event(self.sidebar_remote_access))
        self.sidebar_remote_access.pack(pady=10)
        
        self.sidebar_remote_access.pack_forget()

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

        # configure the container frame to fill any extra space in the sidebar frame
        self.sidebar_container.pack_propagate(0)
        self.sidebar_container.pack(fill="both", expand=True)

        # create create account frame
        self.create_account_frame = CreateAccountFrame(self.main_frame)

        # add items frame
        self.add_items_frame = AddItemsFrame(self.main_frame)

        # view lab server frame
        # self.view_lab_server_frame = ViewLabServerFrame(self.main_frame)

        # remote access frame
        self.remote_access_frame = RemoteAccessFrame(self.main_frame)

        # bind the sidebar button to the create account frame
        self.sidebar_button_event(self.sidebar_register_instructor)

        # default values
        self.appearance_mode_optionemenu.set(self.appearance_mode.capitalize())
        self.scaling_optionemenu.set("100%")

        # style = ttk.Style()
        # style.theme_use("clam")
        # style.configure("Treeview",
        #                 background="#2a2d2e",
        #                 foreground="white",
        #                 rowheight=50,
        #                 fieldbackground="#343638",
        #                 bordercolor="#343638",
        #                 borderwidth=0)
        # style.map('Treeview', background=[('selected', '#22559b')])
        # style.configure("Treeview.Heading",
        #                 background="#565b5e",
        #                 foreground="white",
        #                 relief="flat")
        # style.map("Treeview.Heading",
        #           background=[('active', '#3484F0')])

    # bind the function to the window close event
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.timer_interval = 5000  # 5 seconds
        self.check_for_new_data()
            
    def check_for_new_data(self):
        db = get_database()
        cursor = db.cursor()        
        query = "SELECT user_id, ip_address FROM `active_user_ip` WHERE user_type='instructor' AND is_active=1;"
        cursor.execute(query)
        results = cursor.fetchall()
        
        
        idCursor = db.cursor()        
        idQuery = "SELECT user_instructor.id, CONCAT(user_instructor.last_name, ', ', user_instructor.first_name) AS Name FROM user_instructor INNER JOIN active_user_ip ON active_user_ip.user_id = user_instructor.id;"
        idCursor.execute(idQuery)
        idResults = idCursor.fetchall()
        
        new_text = ''
        
        for result in results:
            user_id, ip_address = result
            for idResult in idResults:
                id, name = idResult
                if id == user_id:
                    new_text += f"{name}: {ip_address}\n"
                    break
                    
        
        self.online_servers_lbl.configure(text=new_text)

        db.close()
        self.sidebar_frame.after(self.timer_interval, self.check_for_new_data)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            close_lan_active(self.id, 0)
            self.destroy()

    def logout_event(self):
        from login import App

        close_lan_active(self.id, 0)

        login_window = App()

        # destroy the current window
        self.destroy()

        # create a new instance of the login window
        login_window.mainloop()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self, button):
        # disable the clicked button and enable all other buttons
        for btn in [self.sidebar_register_instructor, self.sidebar_add_items, self.sidebar_remote_access]:
            if btn == button:
                btn.configure(state="disabled")
            else:
                btn.configure(state="normal")

        # show the specific frame for the clicked button and hide all other frames
        if button == self.sidebar_register_instructor:
            self.create_account_frame.create_account_frame.pack(
                fill="both", expand=True)
            self.add_items_frame.add_items_frame.pack_forget()
            # self.view_lab_server_frame.view_lab_server_frame.pack_forget()
            self.remote_access_frame.remote_access_frame.pack_forget()
        elif button == self.sidebar_add_items:
            self.create_account_frame.create_account_frame.pack_forget()
            self.add_items_frame.add_items_frame.pack(fill="both", expand=True)
            # self.view_lab_server_frame.view_lab_server_frame.pack_forget()
            self.remote_access_frame.remote_access_frame.pack_forget()

            self.remote_access_frame.remote_access_frame.pack_forget()
        elif button == self.sidebar_remote_access:
            self.create_account_frame.create_account_frame.pack_forget()
            self.add_items_frame.add_items_frame.pack_forget()
            # self.view_lab_server_frame.view_lab_server_frame.pack_forget()
            self.remote_access_frame.remote_access_frame.pack(
                fill="both", expand=True)


if __name__ == "__main__":
    app = AdminDashboard()
    app.mainloop()
