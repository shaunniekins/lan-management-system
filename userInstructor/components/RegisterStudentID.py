from tkinter import ttk
from tkinter import messagebox


import customtkinter

from utils.db_connection import get_database


class RegisterStudentID(customtkinter.CTk):
    def __init__(self, sidebar_register_id):
        super().__init__()

        self.btn = sidebar_register_id

        self.geometry("330x280")
        self.resizable(width=False, height=False)

        self.title('Register Student ID')

        self.frame = customtkinter.CTkFrame(self)
        self.frame.pack(fill="both", expand=True)

        self.container = customtkinter.CTkFrame(
            self.frame, corner_radius=0)
        self.container.grid(row=0, column=0, sticky="nsew")

        # configure the grid weights
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # get the width of the container
        container_width = self.container.winfo_reqwidth()

        # center the container horizontally
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        # self.signup_label = customtkinter.CTkLabel(
        #     self.container, text="Register Student ID", font=('Arial Gothic', 20, 'bold'))
        # self.signup_label.grid(
        #     column=0, columnspan=2, row=0, padx=70, pady=(45, 40))

        self.id_label = customtkinter.CTkLabel(self.container, text="Enter ID:").grid(
            column=0, row=1, padx=30, pady=(60, 0), sticky="w")

        self.id_entry = customtkinter.CTkEntry(
            self.container, width=270, height=35, font=('Arial', 20))
        self.id_entry.grid(column=0, columnspan=2, row=2, padx=30)

        self.submit_next_btn = customtkinter.CTkButton(
            self.container, text="Submit and continue", command=self.register_multiple_event, width=130).grid(column=1, row=9, padx=30, pady=(10, 0))

        self.submit_btn = customtkinter.CTkButton(
            self.container, text="Submit and close", command=self.register_event, width=130).grid(column=1, row=10, padx=30, pady=(10, 0))

        self.close_btn = customtkinter.CTkButton(
            self.container, fg_color="white", text_color="black", text="Close", command=self.close_event, width=130).grid(column=1, row=11, padx=30, pady=(10, 30))

    def close_event(self):
        self.btn.configure(state='normal')
        self.destroy()

    def configureBtn(btn):
        btn.configure(state="normal")

    def register_event(self):
        success = self.register_multiple_event()
        if success:
            messagebox.showinfo("Success", "ID registered successfully.")
            self.close_event()

    def register_multiple_event(self):
        id = self.id_entry.get()

        db = get_database()
        cursor = db.cursor()

        if not id:
            messagebox.showerror("Error", "Invalid input.")
            return False
        else:
            query = "SELECT * FROM registered_student_id WHERE student_id = %s"
            values = (id,)
            cursor.execute(query, values)
            result = cursor.fetchone()
            if result:
                messagebox.showerror(
                    "Error", "ID Number already registered.")
                return False
            else:
                query = "INSERT INTO registered_student_id (student_id) VALUES (%s)"
                values = (id,)
                cursor.execute(query, values)

                db.commit()
                cursor.close()
                db.close()
                self.id_entry.delete(0, "end")
                return True
