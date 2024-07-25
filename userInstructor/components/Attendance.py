from tkinter import ttk
from tkinter import messagebox

import customtkinter
import subprocess

import os
from datetime import datetime, date
from fpdf import FPDF
import threading
import time


from utils.db_connection import get_database


class AttendanceFrame:
    def __init__(self, parent_frame, id, full_name):
        self.parent_frame = parent_frame
        self.id = id
        self.name = full_name
        self.subjectToShow = ' '
        self.year_lvl = ' '
        
        self.current_date = date.today()
        
        # Create a timer to periodically update attendance data
        self.timer_interval = 10  # Update every 60 seconds
        self.timer = None
        self.start_timer()
        
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
        # Update the query for retrieving distinct subject descriptions
        querySection = "SELECT DISTINCT registered_subject.subject_description FROM registered_subject JOIN user_instructor ON registered_subject.instructor = user_instructor.id WHERE user_instructor.id = %s AND registered_subject.subject_description != '' ORDER BY registered_subject.subject_description;"
        valuesSection = (self.id,)
        cursorSection.execute(querySection, valuesSection)
        resultSection = cursorSection.fetchall()
        # self.optionsSubject = ["All sections"] + [row[0]
        #                                         for row in resultSection]
        self.optionsSubject = [row[0] for row in resultSection]

        self.attendance_option = customtkinter.CTkOptionMenu(
            self.attendance_left_container, values=self.optionsSubject, width=200, command=self.update_attendance_subject)
        self.attendance_option.grid(row=1, column=1, padx=5, pady=5)

        self.attendance_option.bind(
            "<<ComboboxSelected>>", self.update_attendance_subject)
        
        self.course_label = customtkinter.CTkLabel(
            master=self.attendance_left_container,
            text=' ',
            # font=customtkinter.CTkFont(size=15, weight="normal")
            )
        self.course_label.grid(row=2, column=1, padx=5, pady=5)
        self.course_label.grid_remove()
        
        self.print_data = customtkinter.CTkButton(
            self.attendance_left_container, fg_color="green", text="🖨️ Print", width=200)
        self.print_data.grid(row=3, column=1, padx=5, pady=5)
        

        self.attendance_option.bind(
            "<<ComboboxSelected>>")

        # create the Treeview object
        """
        TABLE (RIGHT CONTAINER)
        """

        # create the table
        # self.subjectColumn = ('Name','Date', 'Time', 'Subject', 'Course')
        self.subjectColumn = ('Name', 'Time In', 'Time Out')

        self.attendanceTable = ttk.Treeview(self.attendance_right_container,
                                         columns=self.subjectColumn,
                                         height=17,
                                         selectmode='browse',
                                         show='headings')

        self.attendanceTable.column("#1", anchor="c", width=30)
        self.attendanceTable.column("#2", anchor="c", width=10)
        self.attendanceTable.column("#3", anchor="c", width=10)
      

        self.attendanceTable.heading('Name', text='Name')
        # self.attendanceTable.heading('Section', text='Section')
        self.attendanceTable.heading('Time In', text='Time In')
        self.attendanceTable.heading('Time Out', text='Time Out')
        # self.attendanceTable.heading('Subject', text='Subject')
        # self.attendanceTable.heading('Course', text='Course')
        

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

        self.subjectToShow = self.attendance_option.get()
        if self.subjectToShow == "All sections":
            # Update the query for retrieving attendance data for all sections
            query = (
                "SELECT CONCAT(user_student.last_name, ', ', user_student.first_name) AS name, student_attendance.date, student_attendance.time_in, student_attendance.time_out "
                "FROM student_attendance "
                "JOIN enrolled_subject ON student_attendance.student_number = enrolled_subject.student "
                "JOIN registered_subject ON enrolled_subject.subject = registered_subject.id "
                "JOIN user_student ON enrolled_subject.student = user_student.id "
                "JOIN user_instructor ON registered_subject.instructor = user_instructor.id "
                "WHERE registered_subject.subject_description != '' AND enrolled_subject.section != '' "
                "ORDER BY student_attendance.date DESC, student_attendance.time_in ASC;"
            )

            values = (self.id,)
        else:
            # student_attendance.date, registered_subject.subject_description, registered_subject.course_description
            queryCourseDisplay = (
                "SELECT course_description, year_level, section "
                "FROM registered_subject "
                "WHERE instructor = %s AND subject_description = %s "
                "AND course_description != '' AND year_level != '' AND section != '';"
            )
            valuesCourseDisplay = (self.id, self.subjectToShow)
                        
            query = (
                # , registered_subject.section, 
                "SELECT CONCAT(user_student.last_name,', ', user_student.first_name) as name,"
                "TIME_FORMAT(student_attendance.time_in, '%H:%i') as time_in, "
                "TIME_FORMAT(student_attendance.time_out, '%H:%i') as time_out "
                "FROM student_attendance "
                "JOIN enrolled_subject ON student_attendance.student_number = enrolled_subject.student "
                "JOIN registered_subject ON enrolled_subject.subject = registered_subject.id "
                "JOIN user_student ON enrolled_subject.student = user_student.id "
                "JOIN user_instructor ON registered_subject.instructor = user_instructor.id "
                "WHERE user_instructor.id = %s "
                "AND registered_subject.subject_description = %s"
                "AND DATE(student_attendance.date) = %s " 
                "ORDER BY user_student.last_name DESC;"
            )
            values = (self.id, self.subjectToShow, self.current_date)
            # print('self.current_date: ', self.current_date)

        db = get_database()
        
        cursorCourseDisplay = db.cursor()
        cursorCourseDisplay.execute(queryCourseDisplay, valuesCourseDisplay)
        # Fetch the result from the cursor
        result = cursorCourseDisplay.fetchone()
        if result is not None:
            course_description = result[0]
            year_level = result[1]
            section = result[2]
        else:
            course_description = ''
            year_level = ''
            section = ''
        
        self.year_lvl = year_level
        self.course_label.configure(text=f'{course_description} - {section}')
        self.course_label.grid(row=2, column=1, padx=5, pady=5)
        
        cursor = db.cursor()
        cursor.execute(query, values)
        
        for row in cursor:
            self.attendanceTable.insert('', 'end', values=row)


        cursorCourseDisplay.close()
        cursor.close()
        db.close()
        
        self.start_timer()

    def print_table(self):
        formatted_date = self.current_date.strftime('%B %d, %Y')
        
        course_label_text = self.course_label.cget("text")
        # create PDF document
        pdf = FPDF("P", "mm", "A4")
        # add a page
        pdf.add_page()
        
        available_fonts = FPDF().core_fonts
        font = 'Bookman Old Style' if 'bookman' in available_fonts else 'Times'
        
        pdf.image('assets/asscat_logo.jpg', x=10, y=8, w=18, h=18)
        pdf.set_font(font, 'B', 11)
        pdf.cell(0, 5, 'AGUSAN DEL SUR STATE COLLEGE OF AGRICULTURE AND TECHNOLOGY', ln=True, align='C')
        pdf.cell(0, 10, 'STUDENT ATTENDANCE', ln=True, align='C')
        
        pdf.ln(8)
        
        pdf.set_font(font, '', 11)
        pdf.cell(0, 5, f'Instructor: {self.name}', align='L')
        pdf.cell(0, 5, f'Date: {formatted_date}', align='R', ln=True)
        pdf.cell(0, 5, f'Subject: {self.subjectToShow}', ln=True) 
        pdf.cell(0, 5, f'Year level: {self.year_lvl}', ln=True)
        pdf.cell(0, 5, f'Course & Section: {course_label_text}', ln=True) 


        pdf.ln(10)

        # calculate available horizontal space
        available_width = pdf.w - 2 * pdf.l_margin

        # calculate column width based on the available space
        column_width = available_width / len(self.subjectColumn)

        # add table header
        pdf.set_font(font, 'B', 11)
        for column in self.subjectColumn:
            pdf.cell(column_width, 10, column, border=1, align='C')

        pdf.ln()

        # add table data
        pdf.set_font('Times', '', 12)  # Set font to regular
        for row in self.attendanceTable.get_children():
            values = self.attendanceTable.item(row)['values']
            for value in values:
                pdf.cell(column_width, 10, str(value), border=1, align='C')
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
        messagebox.showinfo("PDF Saved", f"Attendance PDF saved as:\n{file_name}")

    def start_timer(self):
        self.stop_timer()  # Stop the timer if it's already running
        self.timer = threading.Timer(self.timer_interval, self.update_attendance_subject, args=(None,))
        self.timer.start()

    def stop_timer(self):
        if self.timer and self.timer.is_alive():
            self.timer.cancel()
            self.timer = None