from tkinter import ttk
from tkinter import messagebox

import customtkinter

from utils.db_connection import get_database


class AddItemsFrame:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame

        self.add_items_frame = customtkinter.CTkScrollableFrame(
            self.parent_frame)

        # create container for subject
        self.subject_container = customtkinter.CTkFrame(
            self.add_items_frame, corner_radius=0)
        self.subject_container.grid(row=0, column=0, sticky="nsew")

        # create container for course
        self.course_container = customtkinter.CTkFrame(
            self.add_items_frame, corner_radius=0)
        self.course_container.grid(row=0, column=1, sticky="nsew")

        # create container for school year
        self.school_year_container = customtkinter.CTkFrame(
            self.add_items_frame, corner_radius=0)
        self.school_year_container.grid(row=0, column=2, sticky="nsew")

        # configure grid columns to expand equally
        self.add_items_frame.grid_columnconfigure(0, weight=1)
        self.add_items_frame.grid_columnconfigure(1, weight=1)
        self.add_items_frame.grid_columnconfigure(2, weight=1)

        """
        SUBJECT COMPONENTS
        """

        # top subject container
        # self.subject_top_container = customtkinter.CTkFrame(
        #     self.subject_container, corner_radius=0)
        # self.subject_top_container.pack_propagate(0)
        # self.subject_top_container.pack(side="top", fill="y", expand=True)

        # """
        self.subject_top_container = customtkinter.CTkFrame(
            self.subject_container, corner_radius=0)
        self.subject_top_container.pack(side="top", fill="both", expand=True)
        # """

        # bottom subject container
        self.subject_bottom_container = customtkinter.CTkFrame(
            self.subject_container, corner_radius=0)
        self.subject_bottom_container.pack(
            side="bottom", fill="both", expand=True)

        self.subject_label = customtkinter.CTkLabel(
            self.subject_top_container, text="Subject", font=('Arial', 20, 'bold'))
        self.subject_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.add_subject_code_label = customtkinter.CTkLabel(
            self.subject_top_container, text="Code:")
        self.add_subject_code_label.grid(
            row=1, column=0,  padx=5, pady=5)
        self.add_subject_code_entry = customtkinter.CTkEntry(
            self.subject_top_container, width=200)
        self.add_subject_code_entry.grid(row=1, column=1, padx=5, pady=5)

        self.add_subject_desc_label = customtkinter.CTkLabel(
            self.subject_top_container, text="Description:")
        self.add_subject_desc_label.grid(row=2, column=0, padx=5, pady=5)
        self.add_subject_desc_entry = customtkinter.CTkEntry(
            self.subject_top_container, width=200)
        self.add_subject_desc_entry.grid(row=2, column=1, padx=5, pady=5)

        self.submit_subject_button = customtkinter.CTkButton(
            self.subject_top_container, text="Submit", command=self.subject_submit)
        self.submit_subject_button.grid(
            row=5, column=1, padx=5, pady=5)

        """
        TABLE (BOTTOM CONTAINER)
        """

        subjectColumn = ('code', 'description')

        self.subjectTable = ttk.Treeview(self.subject_bottom_container,
                                         columns=subjectColumn,
                                         height=17,
                                         selectmode='browse',
                                         show='headings',
                                         style="Treeview")

        self.subjectTable = ttk.Treeview(self.subject_bottom_container,
                                         columns=subjectColumn,
                                         height=17,
                                         selectmode='browse',
                                         show='headings')
        self.subjectTable.column("#1", anchor="c", width=20)
        self.subjectTable.column("#2", anchor="c", width=80)
        self.subjectTable.heading('code', text='Subject Code')
        self.subjectTable.heading('description', text='Subject Description')

        self.subjectTable.grid(row=0, column=0, sticky="nsew")

        self.subject_bottom_container.grid_rowconfigure(0, weight=1)
        self.subject_bottom_container.grid_columnconfigure(0, weight=1)

        db = get_database()
        cursor = db.cursor()

        query = "SELECT code, description FROM avail_subject ORDER BY code;"
        cursor.execute(query)

        for row in cursor:
            self.subjectTable.insert('', 'end', values=row)

        cursor.close()
        db.close()

        self.subjectTable.grid(row=0, column=0, columnspan=2,
                               sticky='nsew', padx=10, pady=10)

        self.subjectTable.bind('<Motion>', 'break')

        """
        COURSE COMPONENTS
        """

        # top course container
        # self.course_top_container = customtkinter.CTkFrame(
        #     self.course_container, corner_radius=0)
        # self.course_top_container.pack_propagate(0)
        # self.course_top_container.pack(side="top", fill="y", expand=True)

        # """
        self.course_top_container = customtkinter.CTkFrame(
            self.course_container, corner_radius=0)
        self.course_top_container.pack(side="top", fill="both", expand=True)
        # """

        # bottom course container
        self.course_bottom_container = customtkinter.CTkFrame(
            self.course_container, corner_radius=0)
        self.course_bottom_container.pack(
            side="bottom", fill="both", expand=True)

        self.course_label = customtkinter.CTkLabel(
            self.course_top_container, text="Course", font=('Arial', 20, 'bold'))
        self.course_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.add_course_code_label = customtkinter.CTkLabel(
            self.course_top_container, text="Code:")
        self.add_course_code_label.grid(
            row=1, column=0,  padx=5, pady=5)
        self.add_course_code_entry = customtkinter.CTkEntry(
            self.course_top_container, width=200)
        self.add_course_code_entry.grid(row=1, column=1, padx=5, pady=5)

        self.add_course_desc_label = customtkinter.CTkLabel(
            self.course_top_container, text="Description:")
        self.add_course_desc_label.grid(row=2, column=0, padx=5, pady=5)
        self.add_course_desc_entry = customtkinter.CTkEntry(
            self.course_top_container, width=200)
        self.add_course_desc_entry.grid(row=2, column=1, padx=5, pady=5)

        self.submit_course_button = customtkinter.CTkButton(
            self.course_top_container, text="Submit", command=self.course_submit)
        self.submit_course_button.grid(
            row=5, column=1, padx=5, pady=5)

        courseColumn = ('code', 'description')

        self.courseTable = ttk.Treeview(self.course_bottom_container,
                                        columns=courseColumn,
                                        height=17,
                                        selectmode='browse',
                                        show='headings',
                                        style="Treeview")

        self.courseTable = ttk.Treeview(self.course_bottom_container,
                                        columns=courseColumn,
                                        height=17,
                                        selectmode='browse',
                                        show='headings')
        self.courseTable.column("#1", anchor="c", width=20)
        self.courseTable.column("#2", anchor="c", width=80)
        self.courseTable.heading('code', text='Course Code')
        self.courseTable.heading('description', text='Course Description')

        self.courseTable.grid(row=0, column=0, sticky="nsew")

        self.course_bottom_container.grid_rowconfigure(0, weight=1)
        self.course_bottom_container.grid_columnconfigure(0, weight=1)

        db = get_database()
        cursor = db.cursor()

        query = "SELECT code, description FROM avail_course ORDER BY code;"
        cursor.execute(query)

        for row in cursor:
            self.courseTable.insert('', 'end', values=row)

        cursor.close()
        db.close()

        self.courseTable.grid(row=0, column=0, columnspan=2,
                              sticky='nsew', padx=10, pady=10)

        self.courseTable.bind('<Motion>', 'break')

        """
        SCHOOL-YEAR COMPONENTS
        """

        # top school-year container
        # self.school_year_top_container = customtkinter.CTkFrame(
        #     self.school_year_container, corner_radius=0)
        # self.school_year_top_container.pack_propagate(0)
        # self.school_year_top_container.pack(side="top", fill="y", expand=True)

        # """
        self.school_year_top_container = customtkinter.CTkFrame(
            self.school_year_container, corner_radius=0)
        self.school_year_top_container.pack(
            side="top", fill="both", expand=True)
        # """

        # bottom school-year container
        self.school_year_bottom_container = customtkinter.CTkFrame(
            self.school_year_container, corner_radius=0)
        self.school_year_bottom_container.pack(
            side="bottom", fill="both", expand=True)

        self.school_year_label = customtkinter.CTkLabel(
            self.school_year_top_container, text="School Year", font=('Arial', 20, 'bold'))
        self.school_year_label.grid(
            row=0, column=0, columnspan=2, padx=5, pady=5)

        self.add_school_year_val_label = customtkinter.CTkLabel(
            self.school_year_top_container, text="S.Y.:")
        self.add_school_year_val_label.grid(
            row=1, column=0,  padx=5, pady=5)
        self.add_school_year_val_entry = customtkinter.CTkEntry(
            self.school_year_top_container, width=200)
        self.add_school_year_val_entry.grid(row=1, column=1, padx=5, pady=5)

        self.add_school_year_sem_label = customtkinter.CTkLabel(
            self.school_year_top_container, text="Semester:")
        self.add_school_year_sem_label.grid(row=2, column=0, padx=5, pady=5)
        self.add_school_year_sem_entry = customtkinter.CTkEntry(
            self.school_year_top_container, width=200)
        self.add_school_year_sem_entry.grid(row=2, column=1, padx=5, pady=5)

        self.submit_school_year_button = customtkinter.CTkButton(
            self.school_year_top_container, text="Submit", command=self.school_year_submit)
        self.submit_school_year_button.grid(
            row=5, column=1, padx=5, pady=5)

        school_yearColumn = ('school_year', 'semester')

        self.schoolYearTable = ttk.Treeview(self.school_year_bottom_container,
                                            columns=school_yearColumn,
                                            height=17,
                                            selectmode='browse',
                                            show='headings',
                                            style="Treeview")

        self.schoolYearTable = ttk.Treeview(self.school_year_bottom_container,
                                            columns=school_yearColumn,
                                            height=17,
                                            selectmode='browse',
                                            show='headings')
        self.schoolYearTable.column("#1", anchor="c", width=120)
        self.schoolYearTable.column("#2", anchor="c", width=120)
        self.schoolYearTable.heading('school_year', text='S.Y.')
        self.schoolYearTable.heading('semester', text='Semester')

        self.schoolYearTable.grid(row=0, column=0, sticky="nsew")

        self.school_year_bottom_container.grid_rowconfigure(0, weight=1)
        self.school_year_bottom_container.grid_columnconfigure(0, weight=1)

        db = get_database()
        cursor = db.cursor()

        query = "SELECT school_year, semester FROM avail_academic_year ORDER BY school_year DESC, semester ASC;"
        cursor.execute(query)

        for row in cursor:
            self.schoolYearTable.insert('', 'end', values=row)

        cursor.close()
        db.close()

        self.schoolYearTable.grid(row=0, column=0, columnspan=2,
                                  sticky='nsew', padx=10, pady=10)

        self.schoolYearTable.bind('<Motion>', 'break')

    def subject_submit(self):
        code = self.add_subject_code_entry.get()
        description = self.add_subject_desc_entry.get()

        db = get_database()

        cursor = db.cursor()

        if not all([code, description]):
            messagebox.showerror("Error", "Please fill in all the fields.")
        else:
            query = "SELECT * FROM avail_subject WHERE code = %s OR description = %s"
            values = (code, description)
            cursor.execute(query, values)
            result = cursor.fetchone()
            if result:
                if result[1] == code and result[2] == description:
                    messagebox.showerror(
                        "Error", f"{code} and {description} already exist.")
                elif result[1] == code:
                    messagebox.showerror(
                        "Error", f"{code} already exists with a different description.")
                elif result[2] == description:
                    messagebox.showerror(
                        "Error", f"{description} already exists with a different code.")

            else:
                query = "INSERT INTO avail_subject (code, description) VALUES (%s, %s)"
                values = (code, description)
                cursor.execute(query, values)

                db.commit()
                cursor.close()
                db.close()

                self.subjectTable.delete(*self.subjectTable.get_children())

                db = get_database()
                cursor = db.cursor()
                query = "SELECT code, description FROM avail_subject"
                cursor.execute(query)
                for row in cursor:
                    self.subjectTable.insert('', 'end', values=row)
                cursor.close()
                db.close()

                self.add_subject_code_entry.delete(0, "end")
                self.add_subject_desc_entry.delete(0, "end")
                messagebox.showinfo(
                    "Success", "Subject added successfully.")

    def course_submit(self):
        code = self.add_course_code_entry.get()
        description = self.add_course_desc_entry.get()

        db = get_database()

        cursor = db.cursor()

        if not all([code, description]):
            messagebox.showerror("Error", "Please fill in all the fields.")
        else:
            query = "SELECT * FROM avail_course WHERE code = %s OR description = %s"
            values = (code, description)
            cursor.execute(query, values)
            result = cursor.fetchone()
            if result:
                if result[1] == code and result[2] == description:
                    messagebox.showerror(
                        "Error", f"{code} and {description} already exist.")
                elif result[1] == code:
                    messagebox.showerror(
                        "Error", f"{code} already exists with a different description.")
                elif result[2] == description:
                    messagebox.showerror(
                        "Error", f"{description} already exists with a different code.")

            else:
                query = "INSERT INTO avail_course (code, description) VALUES (%s, %s)"
                values = (code, description)
                cursor.execute(query, values)

                db.commit()
                cursor.close()
                db.close()

                self.courseTable.delete(*self.courseTable.get_children())

                db = get_database()
                cursor = db.cursor()
                query = "SELECT code, description FROM avail_course"
                cursor.execute(query)
                for row in cursor:
                    self.courseTable.insert('', 'end', values=row)
                cursor.close()
                db.close()

                self.add_course_code_entry.delete(0, "end")
                self.add_course_desc_entry.delete(0, "end")
                messagebox.showinfo(
                    "Success", "Course added successfully.")

    def school_year_submit(self):
        schoolYear = self.add_school_year_val_entry.get()
        semester = self.add_school_year_sem_entry.get()

        db = get_database()

        cursor = db.cursor()

        if not all([schoolYear, semester]):
            messagebox.showerror("Error", "Please fill in all the fields.")
        else:
            query = "SELECT * FROM avail_academic_year WHERE school_year = %s AND semester = %s"
            values = (schoolYear, semester)
            cursor.execute(query, values)
            result = cursor.fetchone()
            if result:
                messagebox.showerror(
                    "Error", f"{semester} - {schoolYear}  already exist.")

            else:
                query = "INSERT INTO avail_academic_year (school_year, semester) VALUES (%s, %s)"
                values = (schoolYear, semester)
                cursor.execute(query, values)

                db.commit()
                cursor.close()
                db.close()

                self.schoolYearTable.delete(
                    *self.schoolYearTable.get_children())

                db = get_database()
                cursor = db.cursor()
                query = "SELECT school_year, semester FROM avail_academic_year"
                cursor.execute(query)
                for row in cursor:
                    self.schoolYearTable.insert('', 'end', values=row)
                cursor.close()
                db.close()

                self.add_school_year_val_entry.delete(0, "end")
                self.add_school_year_sem_entry.delete(0, "end")
                messagebox.showinfo(
                    "Success", "School Year added successfully.")
