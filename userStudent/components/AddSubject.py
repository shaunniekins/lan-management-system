from tkinter import ttk
from tkinter import messagebox

import customtkinter

from utils.db_connection import get_database


class AddSubjectFrame:
    def __init__(self, parent_frame, id):
        super().__init__()

        self.parent_frame = parent_frame
        self.id = id

        self.add_subject_frame = customtkinter.CTkScrollableFrame(
            self.parent_frame)
        self.add_subject_frame.pack(fill="both", expand=True)

        self.subject_container = customtkinter.CTkFrame(
            self.add_subject_frame, corner_radius=0)
        self.subject_container.grid(row=0, column=0, sticky="nsew")
        self.add_subject_frame.grid_rowconfigure(0, weight=1)
        self.add_subject_frame.grid_columnconfigure(0, weight=1)

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

        self.subject_label = customtkinter.CTkLabel(
            self.subject_left_container, text="Register Subject", font=('Arial', 20, 'bold'))
        self.subject_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.add_school_year_desc_label = customtkinter.CTkLabel(
            self.subject_left_container, text="School Year:")
        self.add_school_year_desc_label.grid(
            row=1, column=0, padx=5, pady=5)

        self.add_semester_desc_label = customtkinter.CTkLabel(
            self.subject_left_container, text="Semester:")
        self.add_semester_desc_label.grid(
            row=2, column=0, padx=5, pady=5)

        self.add_subject_desc_label = customtkinter.CTkLabel(
            self.subject_left_container, text="Subject:")
        self.add_subject_desc_label.grid(
            row=3, column=0, padx=5, pady=5)

        self.add_section_label = customtkinter.CTkLabel(
            self.subject_left_container, text="Section:")
        self.add_section_label.grid(
            row=4, column=0, padx=5, pady=5)

        self.add_instructor_desc_label = customtkinter.CTkLabel(
            self.subject_left_container, text="Instructor:")
        self.add_instructor_desc_label.grid(
            row=5, column=0, padx=5, pady=5)

        db = get_database()
        cursorSchoolYear = db.cursor()
        querySchoolYear = "SELECT DISTINCT academic_school_year FROM registered_subject ORDER BY academic_school_year DESC;"
        cursorSchoolYear.execute(querySchoolYear)
        self.resultSchoolYear = cursorSchoolYear.fetchall()
        self.optionsSchoolYear = [
            "-- Select school year --"] + [row[0] for row in self.resultSchoolYear]

        def update_semester_options(*args):
            selected_school_year = self.add_school_year_desc_entry.get()
            db = get_database()
            cursorSemester = db.cursor()
            querySemester = "SELECT DISTINCT academic_semester FROM registered_subject WHERE academic_school_year = %s ORDER BY academic_semester ASC;"
            values = (selected_school_year,)
            cursorSemester.execute(querySemester, values)
            self.resultsSemester = cursorSemester.fetchall()
            self.optionsSemester = ["-- Select semester --"] + \
                [row[0] for row in self.resultsSemester]
            self.add_semester_desc_entry.configure(values=self.optionsSemester)

        def update_subject_options(*args):
            selected_school_year = self.add_school_year_desc_entry.get()
            selected_semester = self.add_semester_desc_entry.get()

            db = get_database()
            cursorSubject = db.cursor()
            querySubject = "SELECT DISTINCT subject_description FROM registered_subject WHERE academic_school_year=%s AND academic_semester=%s ORDER BY subject_description ASC;"
            values = (selected_school_year, selected_semester)
            cursorSubject.execute(querySubject, values)
            self.resultsSubject = cursorSubject.fetchall()
            self.optionsSubject = ["-- Select subject --"] + \
                [row[0] for row in self.resultsSubject]
            self.add_subject_desc_entry.configure(values=self.optionsSubject)

        def update_section_options(*args):
            selected_school_year = self.add_school_year_desc_entry.get()
            selected_semester = self.add_semester_desc_entry.get()
            selected_subject = self.add_subject_desc_entry.get()

            db = get_database()
            cursorSection = db.cursor()
            querySection = "SELECT DISTINCT section FROM registered_subject WHERE academic_school_year=%s AND academic_semester=%s AND subject_description = %s ORDER BY section ASC;"
            values = (selected_school_year,
                      selected_semester, selected_subject)
            cursorSection.execute(querySection, values)
            self.resultsSection = cursorSection.fetchall()
            self.optionsSection = ["-- Select section --"] + \
                [row[0] for row in self.resultsSection]
            self.add_section_entry.configure(values=self.optionsSection)

        def update_instructor_options(*args):
            selected_school_year = self.add_school_year_desc_entry.get()
            selected_semester = self.add_semester_desc_entry.get()
            selected_subject = self.add_subject_desc_entry.get()
            selected_section = self.add_section_entry.get()

            db = get_database()
            cursorInstructor = db.cursor()
            queryInstructor = "SELECT DISTINCT CONCAT(user_instructor.last_name, ', ', user_instructor.first_name) AS instructor_name FROM registered_subject INNER JOIN user_instructor ON registered_subject.instructor = user_instructor.id WHERE academic_school_year = %s AND academic_semester = %s AND subject_description = %s AND section = %s ORDER BY CONCAT(user_instructor.last_name, ', ', user_instructor.first_name) ASC"
            values = (selected_school_year,
                      selected_semester, selected_subject, selected_section)

            cursorInstructor.execute(queryInstructor, values)
            self.resultsInstructor = cursorInstructor.fetchall()
            self.optionsInstructor = ["-- Select instructor --"] + \
                [row[0] for row in self.resultsInstructor]
            self.add_instructor_entry.configure(values=self.optionsInstructor)

        self.add_school_year_desc_entry = customtkinter.CTkOptionMenu(
            self.subject_left_container, values=self.optionsSchoolYear, width=200, command=update_semester_options)
        self.add_school_year_desc_entry.grid(row=1, column=1, padx=5, pady=5)

        self.optionsSemester = ["-- Select semester --"]
        self.add_semester_desc_entry = customtkinter.CTkOptionMenu(
            self.subject_left_container, values=self.optionsSemester, width=200, command=update_subject_options)
        self.add_semester_desc_entry.grid(row=2, column=1, padx=5, pady=5)

        self.optionsSubject = ["-- Select subject --"]
        self.add_subject_desc_entry = customtkinter.CTkOptionMenu(
            self.subject_left_container, values=self.optionsSubject, width=200, command=update_section_options)
        self.add_subject_desc_entry.grid(row=3, column=1, padx=5, pady=5)

        self.optionsSection = ["-- Select section --"]
        self.add_section_entry = customtkinter.CTkOptionMenu(
            self.subject_left_container, values=self.optionsSection, width=200, command=update_instructor_options)
        self.add_section_entry.grid(row=4, column=1, padx=5, pady=5)

        self.optionsInstructor = ["-- Select instructor --"]
        self.add_instructor_entry = customtkinter.CTkOptionMenu(
            self.subject_left_container, values=self.optionsInstructor, width=200)
        self.add_instructor_entry.grid(row=5, column=1, padx=5, pady=5)

        self.submit_register_subject_button = customtkinter.CTkButton(
            self.subject_left_container, text="Submit", command=self.add_subject_submit, width=200)
        self.submit_register_subject_button.grid(
            row=7, column=1, padx=5, pady=(20, 0))

        """
        TABLE (RIGHT CONTAINER)
        """

        subjectColumn = ('subject_description', 'year_level', 'section',
                         'course_description', 'academic_school_year', 'academic_semester', 'instructor')

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
        self.subjectTable.column("#7", anchor="c", width=60)

        self.subjectTable.heading('subject_description', text='Subject')
        self.subjectTable.heading('year_level', text='Year Level')
        self.subjectTable.heading('section', text='Section')
        self.subjectTable.heading('course_description', text='Course')
        self.subjectTable.heading('academic_school_year', text='School Year')
        self.subjectTable.heading('academic_semester', text='Semester')
        self.subjectTable.heading('instructor', text='Instructor')

        self.subjectTable.grid(row=0, column=0, sticky="nsew")

        self.subject_right_container.grid_rowconfigure(0, weight=1)
        self.subject_right_container.grid_columnconfigure(0, weight=1)

        db = get_database()
        cursor = db.cursor()

        query = "SELECT registered_subject.subject_description, registered_subject.year_level, registered_subject.section, registered_subject.course_description, registered_subject.academic_school_year, registered_subject.academic_semester, CONCAT(user_instructor.first_name, ' ', user_instructor.last_name) AS instructor FROM enrolled_subject INNER JOIN registered_subject ON enrolled_subject.subject = registered_subject.id INNER JOIN user_instructor ON registered_subject.instructor = user_instructor.id WHERE enrolled_subject.student = %s ORDER BY registered_subject.subject_description ASC;"
        values = (self.id,)
        cursor.execute(query, values)

        for row in cursor:
            self.subjectTable.insert('', 'end', values=row)

        cursor.close()
        db.close()

        self.subjectTable.grid(row=0, column=0, columnspan=2,
                               sticky='nsew', padx=10, pady=10)

        self.subjectTable.bind('<Motion>', 'break')

    def add_subject_submit(self):
        school_year_option = self.add_school_year_desc_entry.get()
        semester_option = self.add_semester_desc_entry.get()
        subject_option = self.add_subject_desc_entry.get()
        section_option = self.add_section_entry.get()
        instructor_option = self.add_instructor_entry.get()

        last_name, first_name = instructor_option.split(", ")

        studentID = self.id

        if school_year_option == "-- Select school year --" or semester_option == "-- Select semester --" or subject_option == "-- Select subject --" or section_option == "-- Select section --" or instructor_option == "-- Select instructor --":
            messagebox.showerror(
                "Error: Select option")

        else:
            db = get_database()

            cursorInstructorID = db.cursor()
            queryInstructorId = "SELECT id FROM user_instructor WHERE first_name = %s AND last_name = %s"
            valuesInstructorID = (first_name, last_name,)
            cursorInstructorID.execute(queryInstructorId, valuesInstructorID)
            resultInstructorID = cursorInstructorID.fetchone()

            instructor_id = resultInstructorID[0]

            cursorSubjectID = db.cursor()
            querySubjectID = "SELECT id FROM registered_subject WHERE academic_school_year=%s AND academic_semester=%s AND subject_description=%s AND section=%s AND instructor=%s;"
            valuesSubjectID = (school_year_option,
                               semester_option, subject_option, section_option, instructor_id,)
            cursorSubjectID.execute(querySubjectID, valuesSubjectID)
            resultSubjectID = cursorSubjectID.fetchone()

            # subject_id = resultSubjectID[0]
            if resultSubjectID is not None:
                subject_id = resultSubjectID[0]
            else:
                print("Subject not found")

            cursor = db.cursor()
            query = "SELECT * FROM enrolled_subject WHERE subject = %s AND student = %s"
            values = (subject_id, studentID)
            cursor.execute(query, values)
            result = cursor.fetchone()
            if result:
                messagebox.showerror(
                    "Error", "You already enrolled with it.")
            else:
                query = "INSERT INTO enrolled_subject (subject, student) VALUES (%s, %s)"
                values = (subject_id, studentID)
                cursor.execute(query, values)

                db.commit()
                cursor.close()
                db.close()

                self.subjectTable.delete(
                    *self.subjectTable.get_children())

                db = get_database()
                cursor = db.cursor()
                query = "SELECT registered_subject.subject_description, registered_subject.year_level, registered_subject.section, registered_subject.course_description, registered_subject.academic_school_year, registered_subject.academic_semester, CONCAT(user_instructor.first_name, ' ', user_instructor.last_name) AS instructor FROM enrolled_subject INNER JOIN registered_subject ON enrolled_subject.subject = registered_subject.id INNER JOIN user_instructor ON registered_subject.instructor = user_instructor.id WHERE enrolled_subject.student = %s"
                values = (self.id,)
                cursor.execute(query, values)
                for row in cursor:
                    self.subjectTable.insert('', 'end', values=row)
                cursor.close()
                db.close()

                self.add_school_year_desc_entry.set(self.optionsSubject[0])
                self.add_semester_desc_entry.set(self.optionsSubject[0])
                self.add_subject_desc_entry.set(self.optionsSubject[0])
                self.add_section_entry.set(self.optionsSubject[0])
                self.add_instructor_entry.set(self.optionsSubject[0])

                messagebox.showinfo(
                    "Success", "Subject added successfully.")
