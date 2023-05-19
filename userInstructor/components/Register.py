from tkinter import ttk
from tkinter import messagebox

import customtkinter

from utils.db_connection import get_database


class RegisterFrame:
    def __init__(self, parent_frame, id):
        # super().__init__()

        self.parent_frame = parent_frame
        self.id = id

        self.register_frame = customtkinter.CTkScrollableFrame(
            self.parent_frame)
        self.register_frame.pack(fill="both", expand=True)

        self.subject_container = customtkinter.CTkFrame(
            self.register_frame, corner_radius=0)
        self.subject_container.grid(row=0, column=0, sticky="nsew")
        self.register_frame.grid_rowconfigure(0, weight=1)
        self.register_frame.grid_columnconfigure(0, weight=1)

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
        querySubject = "SELECT description FROM avail_subject ORDER BY description ASC;"
        cursorSubject.execute(querySubject)
        resultsSubject = cursorSubject.fetchall()
        self.optionsSubject = ["-- Select subject --"] + [row[0]
                                                          for row in resultsSubject]

        cursorCourse = db.cursor()
        queryCourse = "SELECT description FROM avail_course ORDER BY description ASC;"
        cursorCourse.execute(queryCourse)
        resultsCourse = cursorCourse.fetchall()
        self.optionsCourse = ["-- Select course --"] + [row[0]
                                                        for row in resultsCourse]

        cursorSchoolYear = db.cursor()
        querySchoolYear = "SELECT school_year FROM avail_academic_year ORDER BY school_year DESC;"
        cursorSchoolYear.execute(querySchoolYear)
        resultsSchoolYear = cursorSchoolYear.fetchall()
        self.optionsSchoolyear = [row[0] for row in resultsSchoolYear]
        self.optionsSchoolyear = list(set(self.optionsSchoolyear))
        self.optionsSchoolyear.insert(0, "-- Select school year --")

        cursorSemester = db.cursor()
        querySemester = "SELECT semester FROM avail_academic_year ORDER BY semester ASC;"
        cursorSemester.execute(querySemester)
        resultsSemester = cursorSemester.fetchall()
        self.optionsSemester = [row[0] for row in resultsSemester]
        self.optionsSemester = list(set(self.optionsSemester))
        self.optionsSemester.insert(0, "-- Select semester --")

        self.subject_label = customtkinter.CTkLabel(
            self.subject_left_container, text="Register Subject", font=('Arial', 20, 'bold'))
        self.subject_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.add_subject_desc_label = customtkinter.CTkLabel(
            self.subject_left_container, text="Subject:")
        self.add_subject_desc_label.grid(
            row=1, column=0, padx=5, pady=5)

        self.add_subject_desc_entry = customtkinter.CTkOptionMenu(
            self.subject_left_container, values=self.optionsSubject, width=200)
        self.add_subject_desc_entry.grid(row=1, column=1, padx=5, pady=5)

        self.add_year_level_label = customtkinter.CTkLabel(
            self.subject_left_container, text="Year Level:")
        self.add_year_level_label.grid(row=2, column=0, padx=5, pady=5)
        self.add_year_level_entry = customtkinter.CTkEntry(
            self.subject_left_container, width=200)
        self.add_year_level_entry.grid(row=2, column=1, padx=5, pady=5)

        self.add_section_label = customtkinter.CTkLabel(
            self.subject_left_container, text="Section:")
        self.add_section_label.grid(row=3, column=0, padx=5, pady=5)
        self.add_section_entry = customtkinter.CTkEntry(
            self.subject_left_container, width=200)
        self.add_section_entry.grid(row=3, column=1, padx=5, pady=5)

        self.add_course_desc_label = customtkinter.CTkLabel(
            self.subject_left_container, text="Course:")
        self.add_course_desc_label.grid(
            row=4, column=0,  padx=5, pady=5)
        self.add_course_desc_entry = customtkinter.CTkOptionMenu(
            self.subject_left_container, values=self.optionsCourse, width=200)
        self.add_course_desc_entry.grid(row=4, column=1, padx=5, pady=5)

        self.add_school_year_label = customtkinter.CTkLabel(
            self.subject_left_container, text="School Year:")
        self.add_school_year_label.grid(
            row=5, column=0,  padx=5, pady=5)
        self.add_school_year_entry = customtkinter.CTkOptionMenu(
            self.subject_left_container, values=self.optionsSchoolyear, width=200)
        self.add_school_year_entry.grid(row=5, column=1, padx=5, pady=5)

        self.add_semester_label = customtkinter.CTkLabel(
            self.subject_left_container, text="Semester:")
        self.add_semester_label.grid(
            row=6, column=0,  padx=6, pady=5)
        self.add_semester_entry = customtkinter.CTkOptionMenu(
            self.subject_left_container, values=self.optionsSemester, width=200)
        self.add_semester_entry.grid(row=6, column=1, padx=5, pady=5)

        self.submit_register_subject_button = customtkinter.CTkButton(
            self.subject_left_container, text="Submit", command=self.register_subject_submit, width=200)
        self.submit_register_subject_button.grid(
            row=7, column=1, padx=5, pady=(20, 0))

        """
        TABLE (RIGHT CONTAINER)
        """

        subjectColumn = ('subject_description', 'year_level', 'section',
                         'course_description', 'academic_school_year', 'academic_semester')

        self.subjectTable = ttk.Treeview(self.subject_right_container,
                                         columns=subjectColumn,
                                         height=17,
                                         selectmode='browse',
                                         show='headings')

        self.subjectTable.column("#1", anchor="c", width=80)
        self.subjectTable.column("#2", anchor="c", width=40)
        self.subjectTable.column("#3", anchor="c", width=60)
        self.subjectTable.column("#4", anchor="c", width=80)
        self.subjectTable.column("#5", anchor="c", width=80)
        self.subjectTable.column("#6", anchor="c", width=70)

        self.subjectTable.heading('subject_description', text='Subject')
        self.subjectTable.heading('year_level', text='Year Level')
        self.subjectTable.heading('section', text='Section')
        self.subjectTable.heading('course_description', text='Course')
        self.subjectTable.heading('academic_school_year', text='School Year')
        self.subjectTable.heading('academic_semester', text='Semester')

        self.subjectTable.grid(row=0, column=0, sticky="nsew")

        self.subject_right_container.grid_rowconfigure(0, weight=1)
        self.subject_right_container.grid_columnconfigure(0, weight=1)

        db = get_database()
        cursor = db.cursor()

        query = "SELECT subject_description, year_level, section, course_description, academic_school_year, academic_semester FROM registered_subject WHERE instructor=%s ORDER BY year_level ASC, subject_description DESC"
        values = (self.id, )
        cursor.execute(query, values)

        for row in cursor:
            self.subjectTable.insert('', 'end', values=row)

        cursor.close()
        db.close()

        self.subjectTable.grid(row=0, column=0, columnspan=2,
                               sticky='nsew', padx=10, pady=10)

        self.subjectTable.bind('<Motion>', 'break')

    def register_subject_submit(self):
        subject_description = self.add_subject_desc_entry.get()
        year_level = self.add_year_level_entry.get()
        section = self.add_section_entry.get()
        course_description = self.add_course_desc_entry.get()
        school_year = self.add_school_year_entry.get()
        semester = self.add_semester_entry.get()
        instructor = self.id

        db = get_database()

        cursor = db.cursor()

        if not all([subject_description, year_level, section, course_description, school_year, semester, instructor]):
            messagebox.showerror("Error", "Please fill in all the fields.")
        else:
            query = "SELECT * FROM registered_subject WHERE subject_description = %s AND section = %s AND course_description = %s AND academic_school_year = %s AND academic_semester = %s"
            values = (subject_description, section,
                      course_description, school_year, semester)
            cursor.execute(query, values)
            result = cursor.fetchone()
            if result:
                messagebox.showerror(
                    "Error", "The data you entered already exists.")
            else:
                query = "INSERT INTO registered_subject (subject_description, year_level, section, course_description, academic_school_year, academic_semester, instructor) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                values = (subject_description, year_level, section,
                          course_description, school_year, semester, instructor)
                cursor.execute(query, values)

                db.commit()
                cursor.close()
                db.close()

                self.subjectTable.delete(*self.subjectTable.get_children())

                db = get_database()
                cursor = db.cursor()
                query = "SELECT subject_description, year_level, section, course_description, academic_school_year, academic_semester FROM registered_subject WHERE instructor=%s ORDER BY year_level ASC, subject_description DESC;"
                values = (self.id, )
                cursor.execute(query, values)
                for row in cursor:
                    self.subjectTable.insert('', 'end', values=row)
                cursor.close()
                db.close()

                self.add_subject_desc_entry.set(self.optionsSubject[0])
                self.add_year_level_entry.delete(0, "end")
                self.add_section_entry.delete(0, "end")
                self.add_course_desc_entry.set(self.optionsCourse[0])
                self.add_school_year_entry.set(self.optionsSchoolyear[0])
                self.add_semester_entry.set(self.optionsSemester[0])
                messagebox.showinfo(
                    "Success", "Course added successfully.")
