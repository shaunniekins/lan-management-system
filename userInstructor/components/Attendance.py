from tkinter import ttk
from tkinter import messagebox

import customtkinter
import subprocess

from utils.db_connection import get_database


class AttendanceFrame:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        
        self.attendance_frame = customtkinter.CTkScrollableFrame(
            self.parent_frame)
        self.attendance_frame.pack(fill="both", expand=True)

        self.attendance_container = customtkinter.CTkFrame(
            self.attendance_frame, corner_radius=0)
        self.attendance_container.grid(row=0, column=0, sticky="nsew")
        self.attendance_frame.grid_rowconfigure(0, weight=1)
        self.attendance_frame.grid_columnconfigure(0, weight=1)

        """
        COMPONENTS
        """

        # left attendance container
        self.attendance_left_container = customtkinter.CTkFrame(
            self.attendance_container, corner_radius=0)
        self.attendance_left_container.grid(row=0, column=0, sticky="nse")
        self.attendance_container.grid_columnconfigure(0, weight=0)

        # right attendance container
        self.attendance_right_container = customtkinter.CTkFrame(
            self.attendance_container, corner_radius=0)
        self.attendance_right_container.grid(row=0, column=1, sticky="nsew")
        self.attendance_container.grid_columnconfigure(1, weight=1)
        

        db = get_database()

        cursorSubject = db.cursor()
        querySubject = "SELECT CONCAT(u.last_name, ', ', u.first_name, ', ', u.last_name) AS name, sa.date, sa.time FROM user_student u JOIN student_attendance sa ON u.id = sa.student_number ORDER BY last_name DESC;"

        # valuesSubject = (self.id,)
        cursorSubject.execute(querySubject)
        resultsSubject = cursorSubject.fetchall()
        self.optionsSubject = ["All subjects"] + [row[0]
                                                  for row in resultsSubject]

        self.attendance_option = customtkinter.CTkOptionMenu(
            self.attendance_left_container, values=self.optionsSubject, width=200)
        self.attendance_option.grid(row=1, column=1, padx=5, pady=5)


        # create the Treeview object
        """
        TABLE (RIGHT CONTAINER)
        """

        # create the table
        self.subjectColumn = ('name', 'date', 'time')

        self.attendanceTable = ttk.Treeview(self.attendance_right_container,
                                         columns=self.subjectColumn,
                                         height=17,
                                         selectmode='browse',
                                         show='headings')

        self.attendanceTable.column("#1", anchor="c", width=100)
        self.attendanceTable.column("#2", anchor="c", width=80)
        self.attendanceTable.column("#3", anchor="c", width=80)

        self.attendanceTable.heading('name', text='Name')
        self.attendanceTable.heading('date', text='Date')
        self.attendanceTable.heading('time', text='Time')

        self.attendanceTable.grid(row=0, column=0, sticky="nsew")
        
        self.attendance_right_container.grid_rowconfigure(0, weight=1)
        self.attendance_right_container.grid_columnconfigure(0, weight=1)

        # # bind the callback function to the OptionMenu object's "<<ComboboxSelected>>" event
        # self.add_subject_desc_entry.bind(
        #     "<<ComboboxSelected>>", self.update_subject_table)

        # initialize the table
        # self.update_subject_table(None)
        
        db = get_database()
        cursor = db.cursor()

        query = "SELECT CONCAT(u.last_name, ', ', u.first_name, ', ', u.last_name) AS name, sa.date, sa.time FROM user_student u JOIN student_attendance sa ON u.id = sa.student_number ORDER BY last_name DESC;"
        cursor.execute(query)

        for row in cursor:
            self.attendanceTable.insert('', 'end', values=row)

        cursor.close()
        db.close()

        self.attendanceTable.grid(row=0, column=0, columnspan=2,
                               sticky='nsew', padx=10, pady=10)

        self.attendanceTable.bind('<Motion>', 'break')

    # def update_subject_table(self, event):
    #     # delete all rows from the table
    #     for row in self.attendanceTable.get_children():
    #         self.attendanceTable.delete(row)

    #     subjectToShow = self.add_subject_desc_entry.get()
    #     if subjectToShow == "All subjects":
    #         query = "SELECT registered_subject.subject_description, registered_subject.section, registered_subject.year_level, CONCAT(user_student.first_name, ' ', user_student.last_name), registered_subject.academic_school_year, registered_subject.academic_semester FROM registered_subject JOIN enrolled_subject ON registered_subject.id = enrolled_subject.subject JOIN user_student ON enrolled_subject.student = user_student.id WHERE registered_subject.instructor = %s ORDER BY registered_subject.subject_description ASC, registered_subject.section ASC;"
    #         values = (self.id,)
    #     else:
    #         query = "SELECT registered_subject.section, registered_subject.year_level, CONCAT(user_student.first_name, ' ', user_student.last_name), registered_subject.academic_school_year, registered_subject.academic_semester FROM registered_subject JOIN enrolled_subject ON registered_subject.id = enrolled_subject.subject JOIN user_student ON enrolled_subject.student = user_student.id WHERE registered_subject.instructor = %s AND registered_subject.subject_description = %s ORDER BY registered_subject.section ASC, registered_subject.section ASC;"
    #         values = (self.id, subjectToShow)

    #     db = get_database()
    #     cursor = db.cursor()
    #     cursor.execute(query, values)

    #     for row in cursor:
    #         self.attendanceTable.insert('', 'end', values=row)

    #     cursor.close()
    #     db.close()
