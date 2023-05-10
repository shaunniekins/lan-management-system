from tkinter import ttk
from tkinter import messagebox


import customtkinter

from utils.db_connection import get_database

appearance_mode = "system"
customtkinter.set_appearance_mode(appearance_mode)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("450x700")
        self.resizable(width=False, height=False)

        self.title('Create Account - LAN Connect')

        self.frame = customtkinter.CTkFrame(self)
        self.frame.pack(fill="both", expand=True)

        self.container = customtkinter.CTkFrame(
            self.frame, corner_radius=0)
        self.container.grid(row=0, column=0, sticky="nsew")

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        container_width = self.container.winfo_reqwidth()

        self.container.place(relx=0.5, rely=0.5, anchor="center")

        self.signup_label = customtkinter.CTkLabel(
            self.container, text="SIGNUP", font=('Century Gothic', 20, 'bold'), cursor="hand2")
        self.signup_label.grid(
            column=0, columnspan=2, row=0, padx=5, pady=30, sticky="nsew")
        self.signup_label.bind("<Button-1>", self.toggle_appearance_mode)

        # Add labels for form fields
        self.last_name_label = customtkinter.CTkLabel(self.container, text="Last Name:").grid(
            column=0, row=1, padx=(30, 15), pady=15, sticky="w")
        self.middle_name_label = customtkinter.CTkLabel(self.container, text="Middle Name:").grid(
            column=0, row=2, padx=(30, 15), pady=15, sticky="w")
        self.first_name_label = customtkinter.CTkLabel(self.container, text="First Name:").grid(
            column=0, row=3, padx=(30, 15), pady=15, sticky="w")
        self.id_number_label = customtkinter.CTkLabel(self.container, text="ID Number:").grid(
            column=0, row=4, padx=(30, 15), pady=15, sticky="w")
        self.year_level_label = customtkinter.CTkLabel(self.container, text="Year Level:").grid(
            column=0, row=5, padx=(30, 15), pady=15, sticky="w")
        self.user_name_label = customtkinter.CTkLabel(self.container, text="User Name:").grid(
            column=0, row=6, padx=(30, 15), pady=15, sticky="w")
        self.password_label = customtkinter.CTkLabel(self.container, text="Password:").grid(
            column=0, row=7, padx=(30, 15), pady=15, sticky="w")
        self.confirm_password_label = customtkinter.CTkLabel(self.container, text="Confirm Password:").grid(
            column=0, row=8, padx=(30, 15), pady=15, sticky="w")

        # Add entry fields for form fields
        self.last_name_entry = customtkinter.CTkEntry(
            self.container, width=250, height=35)
        self.last_name_entry.grid(column=1, row=1, padx=(5, 30), pady=5)

        self.middle_name_entry = customtkinter.CTkEntry(
            self.container, width=250, height=35)
        self.middle_name_entry.grid(
            column=1, row=2, padx=(5, 30), pady=5)
        self.first_name_entry = customtkinter.CTkEntry(
            self.container, width=250, height=35)
        self.first_name_entry.grid(column=1, row=3, padx=(5, 30), pady=5)
        self.id_number_entry = customtkinter.CTkEntry(
            self.container, width=250, height=35)
        self.id_number_entry.grid(column=1, row=4, padx=(5, 30), pady=5)

        self.year_level_entry = customtkinter.CTkEntry(
            self.container, width=250, height=35)
        self.year_level_entry.grid(column=1, row=5, padx=(5, 30), pady=5)

        self.user_name_entry = customtkinter.CTkEntry(
            self.container, width=250, height=35)
        self.user_name_entry.grid(column=1, row=6, padx=(5, 30), pady=5)

        self.password_entry = customtkinter.CTkEntry(
            self.container, width=250, height=35, show="*")
        self.password_entry.grid(column=1, row=7, padx=(5, 30), pady=5)

        self.confirm_password_entry = customtkinter.CTkEntry(
            self.container, width=250, height=35, show="*")
        self.confirm_password_entry.grid(column=1, row=8, padx=(5, 30), pady=5)

        # Add submit button
        self.submit_btn = customtkinter.CTkButton(
            self.container, width=250, height=35, text="Submit", command=self.create_account,).grid(column=1, row=9, padx=(5, 30), pady=(25, 0))

        self.cancel_btn = customtkinter.CTkButton(
            self.container, width=250, height=35, fg_color="white", text_color="black", text="Cancel", command=self.cancel_event,).grid(column=1, row=10, padx=(5, 30), pady=(10, 30))

    def toggle_appearance_mode(self, event):
        global appearance_mode
        if appearance_mode == "system":
            appearance_mode = "light"
        else:
            appearance_mode = "system"
        customtkinter.set_appearance_mode(appearance_mode)

    def cancel_event(self):
        from login import App

        login_window = App()
        self.destroy()
        login_window.mainloop()

    def create_account(self):
        last_name = self.last_name_entry.get()
        middle_name = self.middle_name_entry.get()
        first_name = self.first_name_entry.get()
        id_number = self.id_number_entry.get()
        year_level = self.year_level_entry.get()
        username = self.user_name_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        db = get_database()
        cursor = db.cursor()

        if not all([last_name, middle_name, first_name, id_number, year_level, username, password, confirm_password]):
            messagebox.showerror("Error", "Please fill in all the fields.")
        elif password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
        else:
            # check if id number if registered by instructor
            query = "SELECT * FROM registered_student_id WHERE student_id = %s"
            values = (id_number,)
            cursor.execute(query, values)
            result = cursor.fetchone()
            if not result:
                messagebox.showerror(
                    "Error", f"{id_number}: Not registered by an instructor.")
            else:
                # check if id number if already used
                query = "SELECT * FROM user_student WHERE id_number = %s"
                values = (id_number,)
                cursor.execute(query, values)
                result = cursor.fetchone()
                if result:
                    messagebox.showerror(
                        "Error", f"{id_number} already used by an account.")
                else:
                    query = "SELECT * FROM user_student WHERE first_name = %s AND last_name = %s"
                    values = (first_name, last_name)
                    cursor.execute(query, values)
                    result = cursor.fetchone()
                    if result:
                        messagebox.showerror(
                            "Error", f"{first_name} {last_name} already exists.")
                    else:
                        query = "SELECT * FROM user_instructor WHERE username = %s"
                        values = (username,)
                        cursor.execute(query, values)
                        result = cursor.fetchone()
                        if result:
                            messagebox.showerror(
                                "Error", "Username already exists.")
                        else:
                            query = "SELECT * FROM user_student WHERE username = %s"
                            values = (username,)
                            cursor.execute(query, values)
                            result = cursor.fetchone()
                            if result:
                                messagebox.showerror(
                                    "Error", "Username already exists.")
                            else:
                                query = "SELECT * FROM user_admin WHERE username = %s"
                                values = (username,)
                                cursor.execute(query, values)
                                result = cursor.fetchone()
                                if result:
                                    messagebox.showerror(
                                        "Error", "Username already exists.")
                                else:
                                    query = "INSERT INTO user_student (id_number, username, first_name, middle_name, last_name, year_level, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                                    values = (id_number, username, first_name,
                                              middle_name, last_name, year_level, password)
                                    cursor.execute(query, values)

                                    db.commit()
                                    cursor.close()
                                    db.close()

                                    # clear the entry widgets
                                    self.last_name_entry.delete(0, "end")
                                    self.middle_name_entry.delete(0, "end")
                                    self.first_name_entry.delete(0, "end")
                                    self.id_number_entry.delete(0, "end")
                                    self.year_level_entry.delete(0, "end")
                                    self.user_name_entry.delete(0, "end")
                                    self.password_entry.delete(0, "end")
                                    self.confirm_password_entry.delete(
                                        0, "end")

                                    messagebox.showinfo(
                                        "Success", "Account created successfully.")
                                    self.cancel_event()
