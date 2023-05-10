from tkinter import ttk
from tkinter import messagebox

import customtkinter
import subprocess

import os
from datetime import datetime
from fpdf import FPDF

from utils.db_connection import get_database


class AttendanceFrame:
    def __init__(self, parent_frame, id):
        self.parent_frame = parent_frame
        self.id = id
        
        
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

        cursorSection = db.cursor()
        querySection = "SELECT DISTINCT(registered_subject.section) FROM registered_subject JOIN user_instructor ON registered_subject.instructor = user_instructor.id WHERE user_instructor.id = %s ORDER BY section;"
        valuesSection = (self.id,)
        cursorSection.execute(querySection, valuesSection)
        resultSection = cursorSection.fetchall()
        self.optionsSubject = ["All sections"] + [row[0]
                                                for row in resultSection]


        self.attendance_option = customtkinter.CTkOptionMenu(
            self.attendance_left_container, values=self.optionsSubject, width=200, command=self.update_attendance_subject)
        self.attendance_option.grid(row=1, column=1, padx=5, pady=5)

        self.attendance_option.bind(
            "<<ComboboxSelected>>", self.update_attendance_subject)
        
        self.print_data = customtkinter.CTkButton(
            self.attendance_left_container, fg_color="green", text="🖨️ Print", width=200)
        self.print_data.grid(row=2, column=1, padx=5, pady=5)
        

        self.attendance_option.bind(
            "<<ComboboxSelected>>")

        # create the Treeview object
        """
        TABLE (RIGHT CONTAINER)
        """

        # create the table
        self.subjectColumn = ('name','date', 'time',  'section')

        self.attendanceTable = ttk.Treeview(self.attendance_right_container,
                                         columns=self.subjectColumn,
                                         height=17,
                                         selectmode='browse',
                                         show='headings')

        self.attendanceTable.column("#1", anchor="c", width=100)
        self.attendanceTable.column("#2", anchor="c", width=80)
        self.attendanceTable.column("#3", anchor="c", width=80)
        self.attendanceTable.column("#4", anchor="c", width=80)

        self.attendanceTable.heading('name', text='Name')
        self.attendanceTable.heading('date', text='Date')
        self.attendanceTable.heading('time', text='Time')
        self.attendanceTable.heading('section', text='Section')

        self.attendanceTable.grid(row=0, column=0, sticky="nsew")
        
        self.attendance_right_container.grid_rowconfigure(0, weight=1)
        self.attendance_right_container.grid_columnconfigure(0, weight=1)

        # # bind the callback function to the OptionMenu object's "<<ComboboxSelected>>" event
        self.attendance_option.bind(
            "<<ComboboxSelected>>", self.update_attendance_subject)

        # initialize the table
        self.update_attendance_subject(None)
        self.print_data.configure(command=self.print_table)
        
        
    def update_attendance_subject(self, event):
        # delete all rows from the table
        for row in self.attendanceTable.get_children():
            self.attendanceTable.delete(row)

        subjectToShow = self.attendance_option.get()
        print("attendance123: ", subjectToShow)
        if subjectToShow == "All sections":
            query = (
                "SELECT CONCAT(user_student.first_name,', ', user_student.last_name) as name, student_attendance.date, student_attendance.time, registered_subject.section "
                "FROM student_attendance "
                "JOIN enrolled_subject ON student_attendance.student_number = enrolled_subject.student "
                "JOIN registered_subject ON enrolled_subject.subject = registered_subject.id "
                "JOIN user_student ON enrolled_subject.student = user_student.id "
                "JOIN user_instructor ON registered_subject.instructor = user_instructor.id "
                "WHERE user_instructor.id = %s "
                "ORDER BY student_attendance.date DESC, student_attendance.time DESC;"
            )
            values = (self.id,)
        else:
            query = (
                "SELECT CONCAT(user_student.first_name,', ', user_student.last_name) as name, student_attendance.date, student_attendance.time, registered_subject.section "
                "FROM student_attendance "
                "JOIN enrolled_subject ON student_attendance.student_number = enrolled_subject.student "
                "JOIN registered_subject ON enrolled_subject.subject = registered_subject.id "
                "JOIN user_student ON enrolled_subject.student = user_student.id "
                "JOIN user_instructor ON registered_subject.instructor = user_instructor.id "
                "WHERE user_instructor.id = %s "
                "AND registered_subject.section = %s  -- added condition"
                "ORDER BY student_attendance.date DESC, student_attendance.time DESC;"
            )
            values = (self.id, subjectToShow)

        db = get_database()
        cursor = db.cursor()
        cursor.execute(query, values)

        for row in cursor:
            self.attendanceTable.insert('', 'end', values=row)

        cursor.close()
        db.close()

    def print_table(self):
        # create PDF document
        pdf = FPDF("P", "mm", "A4")
        # add a page 
        pdf.add_page()
        # Set font: Times, normal, size 10
        pdf.set_font('Times','', 12)

        # add table header
        for column in self.subjectColumn:
            pdf.cell(40, 10, column, border=1)

        pdf.ln()

        # add table data
        for row in self.attendanceTable.get_children():
            values = self.attendanceTable.item(row)['values']
            for value in values:
                pdf.cell(40, 10, str(value), border=1)
            pdf.ln()

        # create folder if it doesn't exist
        LAN_FILES_DIR = os.path.expanduser("~/Documents/LAN_Files")
        if not os.path.exists(LAN_FILES_DIR):
            os.makedirs(LAN_FILES_DIR)

        # create file name with current date and time
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d_%H-%M-%S")
        file_name = os.path.join(LAN_FILES_DIR, f"attendance_{date_time}.pdf")

        # save PDF file
        pdf.output(file_name)