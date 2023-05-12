from tkinter import ttk
from tkinter import messagebox

import customtkinter
import subprocess
import os
import signal

from utils.db_connection import get_database


class ViewSubjectFrame:
    def __init__(self, parent_frame, id):
        # super().__init__()

        self.parent_frame = parent_frame
        self.id = id
        
        self.sender_process = None # Initialize sender_process as None


        self.view_subject_frame = customtkinter.CTkScrollableFrame(
            self.parent_frame)
        self.view_subject_frame.pack(fill="both", expand=True)

        self.subject_container = customtkinter.CTkFrame(
            self.view_subject_frame, corner_radius=0)
        self.subject_container.grid(row=0, column=0, sticky="nsew")
        self.view_subject_frame.grid_rowconfigure(0, weight=1)
        self.view_subject_frame.grid_columnconfigure(0, weight=1)

        """
        COMPONENTS
        """

        # left subject container
        self.subject_left_container = customtkinter.CTkFrame(
            self.subject_container, corner_radius=0)
        self.subject_left_container.grid(row=0, column=0, sticky="nse")
        self.subject_container.grid_columnconfigure(0, weight=0)

        # right subject container
        self.subject_right_container = customtkinter.CTkFrame(
            self.subject_container, corner_radius=0)
        self.subject_right_container.grid(row=0, column=1, sticky="nsew")
        self.subject_container.grid_columnconfigure(1, weight=1)

        db = get_database()

        cursorSubject = db.cursor()
        querySubject = "SELECT DISTINCT registered_subject.subject_description FROM registered_subject JOIN enrolled_subject ON registered_subject.id = enrolled_subject.subject JOIN user_student ON enrolled_subject.student = user_student.id WHERE registered_subject.instructor = %s ORDER BY registered_subject.subject_description ASC"
        valuesSubject = (self.id,)
        cursorSubject.execute(querySubject, valuesSubject)
        resultsSubject = cursorSubject.fetchall()
        self.optionsSubject = ["All subjects"] + [row[0]
                                                  for row in resultsSubject]

        self.add_subject_desc_entry = customtkinter.CTkOptionMenu(
            self.subject_left_container, values=self.optionsSubject, width=200, command=self.update_subject_table)
        self.add_subject_desc_entry.grid(row=1, column=1, padx=5, pady=5)


        self.share_screen = customtkinter.CTkButton(
            self.subject_left_container, fg_color="green", text="💻 Share Screen", width=200, command=self.toggle_sender)
        self.share_screen.grid(row=2, column=1, padx=5, pady=5)

        # # bind the callback function to the OptionMenu object's "<<ComboboxSelected>>" event
        self.add_subject_desc_entry.bind(
            "<<ComboboxSelected>>", self.update_subject_table)

        # create the Treeview object
        """
        TABLE (RIGHT CONTAINER)
        """

        # create the table
        self.subjectColumn = ('subject_description', 'section', 'year_level',
                              'students', 'academic_school_year', 'academic_semester')

        self.subjectTable = ttk.Treeview(self.subject_right_container,
                                         columns=self.subjectColumn,
                                         height=17,
                                         selectmode='browse',
                                         show='headings')

        self.subjectTable.column("#1", anchor="c", width=100)
        self.subjectTable.column("#2", anchor="c", width=80)
        self.subjectTable.column("#3", anchor="c", width=80)
        self.subjectTable.column("#4", anchor="c", width=200)
        self.subjectTable.column("#5", anchor="c", width=100)
        self.subjectTable.column("#6", anchor="c", width=80)

        self.subjectTable.heading('subject_description', text='Subject')
        self.subjectTable.heading('section', text='Section')
        self.subjectTable.heading('year_level', text='Year Level')
        self.subjectTable.heading('students', text='Students')
        self.subjectTable.heading(
            'academic_school_year', text='School Year')
        self.subjectTable.heading('academic_semester', text='Semester')

        self.subjectTable.grid(row=0, column=0, sticky="nsew")
        self.subject_right_container.grid_rowconfigure(0, weight=1)
        self.subject_right_container.grid_columnconfigure(0, weight=1)

        # bind the callback function to the OptionMenu object's "<<ComboboxSelected>>" event
        self.add_subject_desc_entry.bind(
            "<<ComboboxSelected>>", self.update_subject_table)

        # initialize the table
        self.update_subject_table(None)

    def update_subject_table(self, event):
        # delete all rows from the table
        for row in self.subjectTable.get_children():
            self.subjectTable.delete(row)

        subjectToShow = self.add_subject_desc_entry.get()
        if subjectToShow == "All subjects":
            query = "SELECT registered_subject.subject_description, registered_subject.section, registered_subject.year_level, CONCAT(user_student.first_name, ' ', user_student.last_name), registered_subject.academic_school_year, registered_subject.academic_semester FROM registered_subject JOIN enrolled_subject ON registered_subject.id = enrolled_subject.subject JOIN user_student ON enrolled_subject.student = user_student.id WHERE registered_subject.instructor = %s ORDER BY registered_subject.subject_description ASC, registered_subject.section ASC;"
            values = (self.id,)
        else:
            query = "SELECT registered_subject.section, registered_subject.year_level, CONCAT(user_student.first_name, ' ', user_student.last_name), registered_subject.academic_school_year, registered_subject.academic_semester FROM registered_subject JOIN enrolled_subject ON registered_subject.id = enrolled_subject.subject JOIN user_student ON enrolled_subject.student = user_student.id WHERE registered_subject.instructor = %s AND registered_subject.subject_description = %s ORDER BY registered_subject.section ASC, registered_subject.section ASC;"
            values = (self.id, subjectToShow)

        db = get_database()
        cursor = db.cursor()
        cursor.execute(query, values)

        for row in cursor:
            self.subjectTable.insert('', 'end', values=row)

        cursor.close()
        db.close()

    def on_close(self):
        subprocess.Popen(["pkill", "-9", "-f", "shared_screen_sender.py"])
        # subprocess.call('taskkill /F /IM python.exe /T /FI "WINDOWTITLE eq shared_screen_sender.py"', shell=True)
        
    def toggle_sender(self):
        if self.sender_process is not None:  # If sender_process is running
            subprocess.Popen(["pkill", "-9", "-f", "shared_screen_sender.py"])
            # subprocess.call('taskkill /F /IM python.exe /T /FI "WINDOWTITLE eq shared_screen_sender.py"', shell=True)
            self.sender_process = None  # Set sender_process to None
            # self.sender_process.wait()  # Wait for the sender process to exit
            self.share_screen.configure(fg_color="green", text="💻 Share Screen")
        else:  # If sender_process is not running
            self.sender_process = subprocess.Popen("python shared_screen_sender.py", shell=True, preexec_fn=os.setpgrp)  # Start the sender_process in a new process group
            # self.sender_process = subprocess.Popen("start python shared_screen_sender.py", shell=True)
            self.share_screen.configure(fg_color="red", text="🚫 Stop Share Screen") 