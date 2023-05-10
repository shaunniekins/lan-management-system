import tkinter
from tkinter import ttk

import customtkinter

from utils.db_connection import get_database
from userAdmin.AdminDashboard import AdminDashboard
from userInstructor.InstructorDashboard import InstructorDashboard
from userStudent.StudentDashboard import StudentDashboard


# Modes: system (default), light, dark
appearance_mode = "dark"
customtkinter.set_appearance_mode(appearance_mode)
# Themes: blue (default), dark-blue, green
# customtkinter.set_default_color_theme("green")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # creating custom tkinter window
        self.geometry("400x380")
        # self.geometry("600x450")

        self.title('Login - LAN Connect')

        self.frame = customtkinter.CTkFrame(
            self, width=450, height=380, corner_radius=20)
        self.frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.login_label = customtkinter.CTkLabel(
            master=self.frame, text="LOGIN", font=('Century Gothic', 20, 'bold'), cursor="hand2")
        self.login_label.place(relx=0.5, y=50, anchor=tkinter.CENTER)
        self.login_label.bind("<Button-1>", self.toggle_appearance_mode)

        self.username_label = customtkinter.CTkLabel(
            master=self.frame, text="Username:")
        self.username_label.place(x=50, y=100)

        self.username_entry = customtkinter.CTkEntry(
            master=self.frame, width=350, height=40, font=("Helvetica", 18))
        self.username_entry.place(x=50, y=125)

        self.password_label = customtkinter.CTkLabel(
            master=self.frame, text="Password:")
        self.password_label.place(x=50, y=170)

        self.password_entry = customtkinter.CTkEntry(
            master=self.frame, width=350, height=40, font=("Helvetica", 18), show="*")
        self.password_entry.place(x=50, y=195)
        self.password_entry.bind("<Return>", lambda event: self.login_event())

        # Submit form button
        self.submit_btn = customtkinter.CTkButton(
            master=self.frame, width=350, height=40, text="Login", command=self.login_event, corner_radius=6)
        self.submit_btn.place(x=50, y=270)

        self.create_account_label = customtkinter.CTkLabel(
            master=self.frame, text="Create Student Account", cursor="hand2", text_color="cyan", font=("Helvetica", 11))
        self.create_account_label.place(
            relx=0.5, y=325, anchor=tkinter.CENTER)
        self.create_account_label.bind(
            "<Button-1>", self.open_create_account_page,)

        # Create a ttk style object
        style = ttk.Style()

        style.theme_use("clam")
        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=50,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=0)
        style.map('Treeview', background=[('selected', '#22559b')])
        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief="flat")
        style.map("Treeview.Heading",
                  background=[('active', '#3484F0')])

    def toggle_appearance_mode(self, event):
        global appearance_mode
        if appearance_mode == "dark":
            appearance_mode = "light"
        else:
            appearance_mode = "dark"
        customtkinter.set_appearance_mode(appearance_mode)

    def open_create_account_page(self, event):
        from create_account import App

        create_account_window = App()
        self.destroy()
        create_account_window.mainloop()

    def login_event(self):
        email = self.username_entry.get()
        password = self.password_entry.get()

        # establish connection to MySQL database
        db = get_database()

        # create cursor object
        cursor = db.cursor()

        # check admin_user table
        query = f"SELECT * FROM user_admin WHERE username = '{email}' AND password = '{password}'"
        cursor.execute(query)
        admin_user = cursor.fetchone()

        # check instructor_user table
        if not admin_user:
            query = f"SELECT * FROM user_instructor WHERE username = '{email}' AND password = '{password}'"
            cursor.execute(query)
            instructor_user = cursor.fetchone()

        # check student_user table
        if not admin_user and not instructor_user:
            query = f"SELECT * FROM user_student WHERE username = '{email}' AND password = '{password}'"
            cursor.execute(query)
            student_user = cursor.fetchone()

        if admin_user:
            # ("Authenticated as admin user")
            query = f"SELECT id, first_name, last_name FROM user_admin WHERE username = '{email}' AND password = '{password}'"
            cursor.execute(query)
            admin_user_data = cursor.fetchone()
            id = admin_user_data[0]
            first_name = admin_user_data[1]
            last_name = admin_user_data[2]
            user_type = "admin"
            dashboard_window = AdminDashboard(
                id, first_name, last_name, appearance_mode, user_type)
            self.destroy()
            dashboard_window.mainloop()
        elif instructor_user:
            # ("Authenticated as instructor user")
            query = f"SELECT id, first_name, last_name FROM user_instructor WHERE username = '{email}' AND password = '{password}'"
            cursor.execute(query)
            instructor_user_data = cursor.fetchone()
            id = instructor_user_data[0]
            first_name = instructor_user_data[1]
            last_name = instructor_user_data[2]
            user_type = "instructor"
            dashboard_window = InstructorDashboard(
                id, first_name, last_name, appearance_mode, user_type)
            self.destroy()
            dashboard_window.mainloop()
        elif student_user:
            # ("Authenticated as student user")
            query = f"SELECT id, first_name, last_name FROM user_student WHERE username = '{email}' AND password = '{password}'"
            cursor.execute(query)
            student_user_data = cursor.fetchone()
            id = student_user_data[0]
            first_name = student_user_data[1]
            last_name = student_user_data[2]
            user_type = "student"
            dashboard_window = StudentDashboard(
                id, first_name, last_name, appearance_mode, user_type)
            self.destroy()
            dashboard_window.mainloop()
        else:
            tkinter.messagebox.showerror(
                "Authentication failed", "Invalid email/username or password")

        # close cursor and database connection
        cursor.close()
        db.close()


if __name__ == "__main__":
    app = App()
    app.mainloop()
