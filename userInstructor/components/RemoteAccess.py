from utils.db_connection import get_database
import customtkinter
import tkinterweb
import tkinter as tk
import socket
import subprocess

class RemoteAccessFrame:
    def __init__(self, parent_frame, id):
        self.parent_frame = parent_frame
        self.id = id
        
        self.remote_access_frame = customtkinter.CTkScrollableFrame(
            self.parent_frame)
        self.remote_access_frame.pack(fill="both", expand=True)

        self.container_remote = customtkinter.CTkFrame(
            self.remote_access_frame)
        self.container_remote.pack(fill='both', expand=True)

        subprocess.Popen(['python', 'remote_control/app.py'])

        self.frames = []
        
        hostname = socket.gethostname()
        ip_address = f'{socket.gethostbyname(hostname)}:5000'
        
        db = get_database()
        cursor = db.cursor()
        query = "SELECT COUNT(user_id) FROM `active_user_ip` WHERE user_type='student' AND is_active=1;"
        cursor.execute(query, )
        result = cursor.fetchone()[0]
        
        print("ip_address: ", ip_address)
        

        # Generate the list of websites with the appropriate number of "google.com" entries
        self.websites = [ip_address for _ in range(int(result))]
        print("website: ", self.websites[0])
        

        # Set the number of frames per row
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
            self.buttonMenu = customtkinter.CTkButton(
                self.frame, text="⋮", font=("Arial", 30, 'bold'), width=2)
            self.buttonMenu.place(relx=1.0, x=-10, y=10, anchor="ne")

            # create a popup menu and add options
            self.popup_menu = tk.Menu(self.buttonMenu, tearoff=0)
            self.popup_menu.add_command(
                label="View", command=lambda website=website: self.view_website(website))
            self.popup_menu.add_command(
                label="Shutdown", command=self.shutdown)

            # bind the popup menu to the button
            def popup(event, popup_menu=self.popup_menu):
                popup_menu.post(event.x_root, event.y_root)

            self.buttonMenu.bind("<Button-1>", popup)

            self.popup_menu.posted = False

            frame_count += 1

            
        # configure the columns to be evenly sized
        for i in range(frames_per_row):
            self.container_remote.grid_columnconfigure(i, weight=1)

    def view_website(self, website):
        # Save the initial grid configuration
        self.initial_grid = [(frame.grid_info(), frame) for frame in self.frames]
        
        frames_per_row = 3
        
        # create a "go back" button to show all frames again
        self.go_back_button = customtkinter.CTkButton(
            self.container_remote, text="⬅ Go Back", font=("Arial", 16), command=self.show_all_frames)
        self.go_back_button.grid(
            row=len(self.frames) // 3 + 1, column=0, columnspan=frames_per_row, pady=10, sticky="ne")
    

        for frame in self.frames:
            # hide all frames except for the one with the selected website
            if frame.current_url != website:
                frame.grid_remove()
            else:
                # show the frame with the selected website
                frame.grid(row=10, column=0,  columnspan=frames_per_row, sticky="sew")



    def show_all_frames(self):
        # Restore the initial grid configuration
        for grid_info, frame in self.initial_grid:
            frame.grid(**grid_info)

        self.go_back_button.destroy()
        
    def on_close(self):
        print("im here on close")
        subprocess.Popen(["pkill", "-9", "-f", "app.py"])

    def shutdown(self):
        """Shutdown the remote access"""
        # add code to shutdown the remote access