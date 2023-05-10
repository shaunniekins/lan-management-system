import tkinter
import tkinter.messagebox
import customtkinter
import mysql.connector

import dashboard

# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("System")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("LAN Connect")
        self.geometry(f"{500}x{500}")
        # self.resizable(False, False)

        # configure grid layout (4x4)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=0)

        for i in range(7):
            self.grid_rowconfigure(i, weight=0)

        self.appearance_button = customtkinter.CTkButton(
            self, text="Dark", command=self.change_appearance_mode_event,  width=10)
        self.appearance_button.grid(row=0, column=2, pady=(
            10, 10),  sticky="e")

        # create login system
        self.login_label = customtkinter.CTkLabel(
            self, text="Log in", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.login_label.grid(row=1, column=1, columnspan=2,
                              pady=(80, 10), sticky="nsew")

        self.email_label = customtkinter.CTkLabel(
            self, text="Email/Username:", anchor="w")
        self.email_label.grid(row=2, column=1, pady=(20, 0),  sticky="nsew")

        self.username_entry = customtkinter.CTkEntry(self)
        self.username_entry.grid(
            row=3, column=1, columnspan=2, ipady=3, sticky="nsew")

        self.password_label = customtkinter.CTkLabel(
            self, text="Password:", anchor="w")
        self.password_label.grid(row=4, column=1, pady=(10, 0), sticky="nsew")

        self.password_entry = customtkinter.CTkEntry(self, show="*")
        self.password_entry.grid(
            row=5, column=1, columnspan=2, ipady=3, sticky="nsew")

        self.login_button = customtkinter.CTkButton(
            self, text="Login", command=self.login_event)
        self.login_button.grid(row=7, column=1, columnspan=2,
                               pady=(50, 0), ipady=5, sticky="nsew")

    def change_appearance_mode_event(self):
        current_mode = customtkinter.get_appearance_mode()
        new_mode = "Light" if current_mode == "Dark" else "Dark"
        customtkinter.set_appearance_mode(new_mode)
        self.appearance_button.configure(text=new_mode)

    def login_event(self):
        email = self.username_entry.get()
        password = self.password_entry.get()

        # establish connection to MySQL database
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Hello_World123",
            database="lan_management_system"
        )

        # create cursor object
        cursor = db.cursor()

        # check admin_user table
        query = f"SELECT * FROM admin_user WHERE username = '{email}' AND password = '{password}'"
        cursor.execute(query)
        admin_user = cursor.fetchone()

        # check instructor_user table
        if not admin_user:
            query = f"SELECT * FROM instructor_user WHERE username = '{email}' AND password = '{password}'"
            cursor.execute(query)
            instructor_user = cursor.fetchone()

        # check student_user table
        if not admin_user and not instructor_user:
            query = f"SELECT * FROM student_user WHERE username = '{email}' AND password = '{password}'"
            cursor.execute(query)
            student_user = cursor.fetchone()

        # close cursor and database connection
        cursor.close()
        db.close()

        # check if user is authenticated
        if admin_user:
            print("Authenticated as admin user")
            # open dashboard for admin user
            dashboard_window = dashboard.AdminDashboard()
            # dashboard_window = dashboard.App()
            self.destroy()
            dashboard_window.mainloop()
        elif instructor_user:
            print("Authenticated as instructor user")
            # open dashboard for instructor user
            # dashboard_window = dashboard.InstructorDashboard()
            dashboard_window = dashboard.App()
            self.destroy()
            dashboard_window.mainloop()
        elif student_user:
            print("Authenticated as student user")
            # open dashboard for student user
            # dashboard_window = dashboard.StudentDashboard()
            dashboard_window = dashboard.App()
            self.destroy()
            dashboard_window.mainloop()
        else:
            # show error message if authentication failed
            tkinter.messagebox.showerror(
                "Authentication failed", "Invalid email/username or password")


if __name__ == "__main__":
    app = App()
    app.mainloop()
