from tkinter import ttk
from tkinter import messagebox

import customtkinter

from utils.db_connection import get_database


class CreateAccountFrame:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame

        # create account frame
        self.create_account_frame = customtkinter.CTkScrollableFrame(
            self.parent_frame)
        # add this line to initialize the object
        self.create_account_frame.pack(fill="both", expand=True)

        # container for left and right container
        self.account_container = customtkinter.CTkFrame(
            self.create_account_frame, corner_radius=0)
        self.account_container.grid(row=0, column=0, sticky="nsew")
        self.create_account_frame.grid_rowconfigure(0, weight=1)
        self.create_account_frame.grid_columnconfigure(0, weight=1)

        # left - form container
        self.left_container = customtkinter.CTkFrame(
            self.account_container, corner_radius=0)
        self.left_container.grid(row=0, column=0, sticky="nse")
        self.account_container.grid_columnconfigure(0, weight=0)

        # right - table container
        self.right_container = customtkinter.CTkFrame(
            self.account_container, corner_radius=0)
        self.right_container.grid(row=0, column=1, sticky="nsew")
        self.account_container.grid_columnconfigure(1, weight=1)

        self.register_label = customtkinter.CTkLabel(
            self.left_container, text="Register Instructor", font=('Arial', 20, 'bold'))
        self.register_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        # first name label and entry widget
        self.first_name_label = customtkinter.CTkLabel(
            self.left_container, text="First Name:")
        self.first_name_label.grid(row=1, column=0, padx=5, pady=5)
        self.first_name_entry = customtkinter.CTkEntry(
            self.left_container, width=200)
        self.first_name_entry.grid(row=1, column=1, padx=5, pady=5)

        # last name label and entry widget
        self.last_name_label = customtkinter.CTkLabel(
            self.left_container, text="Last Name:")
        self.last_name_label.grid(row=2, column=0, padx=5, pady=5)
        self.last_name_entry = customtkinter.CTkEntry(
            self.left_container, width=200)
        self.last_name_entry.grid(row=2, column=1, padx=5, pady=5)

        # username label and entry widget
        self.username_label = customtkinter.CTkLabel(
            self.left_container, text="Username:")
        self.username_label.grid(row=3, column=0, padx=5, pady=5)
        self.username_entry = customtkinter.CTkEntry(
            self.left_container, width=200)
        self.username_entry.grid(row=3, column=1, padx=5, pady=5)

        # password label and entry widget
        self.password_label = customtkinter.CTkLabel(
            self.left_container, text="Password:")
        self.password_label.grid(row=4, column=0, padx=5, pady=5)
        self.password_entry = customtkinter.CTkEntry(
            self.left_container, width=200, show="*")
        self.password_entry.grid(row=4, column=1, padx=5, pady=5)

        # confirm password label and entry widget
        self.confirm_password_label = customtkinter.CTkLabel(
            self.left_container, text="Confirm Password:")
        self.confirm_password_label.grid(row=5, column=0, padx=5, pady=5)
        self.confirm_password_entry = customtkinter.CTkEntry(
            self.left_container, width=200, show="*")
        self.confirm_password_entry.grid(row=5, column=1, padx=5, pady=5)

        # create account button
        self.create_account_button = customtkinter.CTkButton(
            self.left_container, text="Create Account", command=self.create_account, width=200)
        self.create_account_button.grid(
            row=6, column=1, padx=5, pady=(20, 0))

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

        # create a treeview widget for the table
        columns = ('username', 'first_name', 'last_name')

        # Create the Treeview widget and set the style
        self.table = ttk.Treeview(self.right_container,
                                  columns=columns,
                                  height=17,
                                  selectmode='browse',
                                  show='headings',
                                  style="Treeview")
        self.table.column("#1", anchor="c", width=120)
        self.table.column("#2", anchor="c", width=120)
        self.table.column("#3", anchor="c", width=120)
        self.table.heading('username', text='Username')
        self.table.heading('first_name', text='First Name')
        self.table.heading('last_name', text='Last Name')

        # Use the grid geometry manager to add the table to the container
        self.table.grid(row=0, column=0, sticky="nsew")

        # Configure the grid to expand the table to fill the available space
        self.right_container.grid_rowconfigure(0, weight=1)
        self.right_container.grid_columnconfigure(0, weight=1)

        # get a database connection and cursor object
        db = get_database()
        cursor = db.cursor()

        # execute the select query
        query = "SELECT username, first_name, last_name FROM user_instructor ORDER BY username ASC;"
        cursor.execute(query)

        # iterate through the results and insert them into the table
        for row in cursor:
            self.table.insert('', 'end', values=row)

        # close the cursor and database connection
        cursor.close()
        db.close()

        self.table.grid(row=0, column=0, columnspan=2,
                        sticky='nsew', padx=10, pady=10)

        self.table.bind('<Motion>', 'break')

    def create_account(self):
        # get the values from the entry widgets
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # establish connection to MySQL database
        db = get_database()

        # create cursor object
        cursor = db.cursor()

        # validate the form data
        if not all([first_name, last_name, username, password, confirm_password]):
            messagebox.showerror("Error", "Please fill in all the fields.")
        elif password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
        else:
            # check if user already exists
            query = "SELECT * FROM user_instructor WHERE first_name = %s AND last_name = %s"
            values = (first_name, last_name)
            cursor.execute(query, values)
            result = cursor.fetchone()
            if result:
                messagebox.showerror(
                    "Error", f"{first_name} {last_name} already exists.")
            else:
                # check if username already exists in user_instructor table
                query = "SELECT * FROM user_instructor WHERE username = %s"
                values = (username,)
                cursor.execute(query, values)
                result = cursor.fetchone()
                if result:
                    messagebox.showerror("Error", "Username already exists.")
                else:
                    # check if username already exists in user_student table
                    query = "SELECT * FROM user_student WHERE username = %s"
                    values = (username,)
                    cursor.execute(query, values)
                    result = cursor.fetchone()
                    if result:
                        messagebox.showerror(
                            "Error", "Username already exists.")
                    else:
                        # check if username already exists in user_admin table
                        query = "SELECT * FROM user_admin WHERE username = %s"
                        values = (username,)
                        cursor.execute(query, values)
                        result = cursor.fetchone()
                        if result:
                            messagebox.showerror(
                                "Error", "Username already exists.")
                        else:
                            # insert the data into the user_instructor table
                            query = "INSERT INTO user_instructor (first_name, last_name, username, password) VALUES (%s, %s, %s, %s)"
                            values = (first_name, last_name,
                                      username, password)
                            cursor.execute(query, values)

                            # commit the changes and close the cursor and database connection
                            db.commit()
                            cursor.close()
                            db.close()

                            # clear the table
                            self.table.delete(*self.table.get_children())

                            # fetch the updated data from the database and insert it into the table
                            db = get_database()
                            cursor = db.cursor()
                            query = "SELECT username, first_name, last_name FROM user_instructor"
                            cursor.execute(query)
                            for row in cursor:
                                self.table.insert('', 'end', values=row)
                            cursor.close()
                            db.close()

                            # clear the entry widgets
                            self.first_name_entry.delete(0, "end")
                            self.last_name_entry.delete(0, "end")
                            self.username_entry.delete(0, "end")
                            self.password_entry.delete(0, "end")
                            self.confirm_password_entry.delete(0, "end")
                            messagebox.showinfo(
                                "Success", "Account created successfully.")
