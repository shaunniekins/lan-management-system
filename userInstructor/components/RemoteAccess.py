from utils.db_connection import get_database
import webview
import customtkinter
import tkinterweb
import tkinter as tk
# import tkinterweb
# import customtkinter
import webbrowser


class RemoteAccessFrame:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        # remote access frame
        self.remote_access_frame = customtkinter.CTkScrollableFrame(
            self.parent_frame)
        # add this line to initialize the object
        self.remote_access_frame.pack(fill="both", expand=True)

        self.container_remote = customtkinter.CTkFrame(
            self.remote_access_frame)
        self.container_remote.pack(fill='both', expand=True)

        self.frames = []

        self.websites = ['https://www.google.com/', 'https://www.facebook.com/',
                         'https://www.twitter.com/', 'https://github.com/shaunniekins?tab=repositories', 'https://www.linkedin.com/in/shaun-niel-ochavo-97915a232/']

        # set the number of frames per row
        frames_per_row = 3
        frame_count = 0

        for website in self.websites:
            # create a new row if we've reached the maximum number of frames per row
            if frame_count % frames_per_row == 0:
                row = len(self.frames) // frames_per_row
                self.container_remote.grid_rowconfigure(row, weight=1)

            # create a new frame and add it to the current row
            self.frame = tkinterweb.HtmlFrame(
                self.container_remote, width=5, height=5)
            self.frame.load_website(website)
            self.frame.grid(row=len(self.frames) // frames_per_row,
                            column=frame_count % frames_per_row, pady=10, padx=10, sticky="nsew")
            self.frames.append(self.frame)

            # create a new button and place it in the frame
            self.button = customtkinter.CTkButton(
                self.frame, text="⋮", font=("Arial", 30, 'bold'), width=2)
            self.button.place(relx=1.0, x=-10, y=10, anchor="ne")

            # create a popup menu and add options
            self.popup_menu = tk.Menu(self.button, tearoff=0)
            self.popup_menu.add_command(
                label="View", command=lambda website=website: self.view_website(website))
            self.popup_menu.add_command(
                label="Shutdown", command=self.shutdown)

            # bind the popup menu to the button

            def popup(event):
                if self.popup_menu.posted:
                    self.popup_menu.unpost()
                else:
                    self.popup_menu.post(event.x_root, event.y_root)
                self.popup_menu.posted = not self.popup_menu.posted

            self.button.bind("<Button-1>", popup)
            self.popup_menu.posted = False

            frame_count += 1

        # configure the columns to be evenly sized
        for i in range(frames_per_row):
            self.container_remote.grid_columnconfigure(i, weight=1)

    def view_website(self, website):
        print("website: ", website)
        for frame in self.frames:
            # hide all frames except for the one with the selected website
            if frame.current_url != website:
                frame.grid_remove()
            else:
                # show the frame with the selected website
                frame.grid()

        # create a "go back" button to show all frames again
        self.go_back_button = customtkinter.CTkButton(
            self.container_remote, text="⬅ Go Back", font=("Arial", 16), command=self.show_all_frames)
        self.go_back_button.grid(
            row=len(self.frames) // 3 + 1, column=1, pady=10)

        self.frame = tkinterweb.HtmlFrame(
            self.container_remote)
        self.frame.load_website(website)
        self.frame.grid(row=len(self.frames), pady=10, padx=10, sticky="nsew")

    def show_all_frames(self):
        for frame in self.frames:
            frame.grid()
        self.go_back_button.destroy()

    def shutdown(self):
        """Shutdown the remote access"""
        # add code to shutdown the remote access
