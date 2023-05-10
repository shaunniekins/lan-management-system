from tkinter import ttk
from tkinter import messagebox

import customtkinter

from utils.db_connection import get_database


class RemoteAccessFrame:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame

        # remote access frame
        self.remote_access_frame = customtkinter.CTkScrollableFrame(
            self.parent_frame)
        # add this line to initialize the object
        self.remote_access_frame.pack(fill="both", expand=True)
