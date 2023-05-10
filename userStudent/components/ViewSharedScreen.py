from tkinter import ttk
from tkinter import messagebox

import customtkinter
from utils.db_connection import get_database
from shared_screen_receiver import start_receiver, stop_receiver


class ViewSharedScreenFrame(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        self.geometry("300x200")
        self.resizable(width=False, height=False)
        self.title('Connect Server')

        self.frame = customtkinter.CTkFrame(self)
        self.frame.pack(fill="both", expand=True)

        self.container = customtkinter.CTkFrame(self.frame, corner_radius=0)
        self.container.grid(row=0, column=0, sticky="nsew")

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.container.place(relx=0.5, rely=0.5, anchor="center")

        self.signup_label1 = customtkinter.CTkLabel(
            self.container, text="Server Available", font=('Arial Gothic', 20, 'bold'))
        self.signup_label1.grid(column=0, columnspan=2,
                                row=0, padx=70, pady=(45, 40))

        db = get_database()
        cursor = db.cursor()
        query = "SELECT DISTINCT active_user_ip.ip_address, CONCAT(user_instructor.last_name, ', ', user_instructor.first_name) AS instructor_name FROM active_user_ip INNER JOIN user_instructor ON active_user_ip.user_id = user_instructor.id WHERE user_type='instructor' AND is_active=0 ORDER BY CONCAT(user_instructor.last_name, ', ', user_instructor.first_name) ASC;"
        cursor.execute(query)
        self.result = cursor.fetchall()
        self.options = ["-- Select instructor Server --"] + \
            [f"{row[1]} -  {row[0]}" for row in self.result]

        self.select_server_option = customtkinter.CTkOptionMenu(
            self.container, values=self.options, width=200)
        self.select_server_option.grid(
            column=0, row=2, padx=(30, 5), pady=(10, 50))

        self.submit_btn = customtkinter.CTkButton(
            self.container, text="➔", command=self.register_event, width=20)
        self.submit_btn.grid(column=1, row=2, padx=(5, 30), pady=(10, 50))

        self.signup_label2 = customtkinter.CTkLabel(
            self.container, text="Server Connected", font=('Arial Gothic', 20, 'bold'))
        self.signup_label2.grid(column=0, columnspan=2,
                                row=0, padx=70, pady=(45, 40))

        self.cancelBtn = customtkinter.CTkButton(
            self.container, text="Stop Server", command=self.cancel_receiver,  width=20)
        self.cancelBtn.grid(column=0, columnspan=2, row=2, pady=(10, 50))

        self.display = True
        self.update_display()

    def update_display(self):
        if self.display:
            self.signup_label1.grid()
            self.select_server_option.grid()
            self.submit_btn.grid()
            self.signup_label2.grid_remove()
            self.cancelBtn.grid_remove()
        else:
            self.signup_label1.grid_remove()
            self.select_server_option.grid_remove()
            self.submit_btn.grid_remove()
            self.signup_label2.grid()
            self.cancelBtn.grid()

    def cancel_receiver(self):
        stop_receiver()
        self.destroy()

    def close_event(self):
        self.destroy()

    def register_event(self):
        selected_option = self.select_server_option.get()

        if (selected_option == "-- Select instructor Server --"):
            messagebox.showwarning("Warning", "Please select a server")
            return

        # ip_address = selected_option.split(" - ")[1].strip()

        # if not start_receiver("192.168.0.115", 9999):
        #     messagebox.showwarning("Warning", "Failed to connect to server")
        #     return

        # self.display = False
        # # messagebox.showinfo("Success", "Successfully connected to server")
        # self.update_display()

        try:
            ip_address = selected_option.split(" - ")[1].strip()
            self.display = False
            self.update_display()

            ports = [9999, 9998, 9997, 9996, 9995]
            i = 0
            start_receiver(ip_address, ports[i])
            i += 1
            # messagebox.showinfo(
            #     "Server started", f"Streaming server started at {ip_address}:9999")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start server: {e}")
