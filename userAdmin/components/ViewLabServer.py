from tkinter import messagebox
from tkinter import ttk
import customtkinter


# from utils.db_connection import get_database
# from ..utils.db_connection import get_database


class ViewLabServerFrame:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame

        self.view_lab_server_frame = customtkinter.CTkScrollableFrame(
            self.parent_frame)
