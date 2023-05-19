from utils.db_connection import get_database
import customtkinter
import tkinterweb
import tkinter as tk
import socket
import subprocess
import webbrowser
import time

# disable remote control (in instructordashboard: self.remote_access_frame.on_close())
class RemoteAccessFrame:
    def __init__(self, parent_frame, id):
        self.parent_frame = parent_frame
        self.id = id

        # subprocess.Popen(["pkill", "-9", "-f", "app.py"])
        # subprocess.call('taskkill /F /IM python.exe /T /FI "WINDOWTITLE eq app.py"', shell=True)
        
        self.remote_access_frame = customtkinter.CTkScrollableFrame(
            self.parent_frame)
        self.remote_access_frame.pack(fill="both", expand=True)

        self.container_remote = customtkinter.CTkFrame(
            self.remote_access_frame)
        self.container_remote.pack(fill='both', expand=True)

    #     hostname = socket.gethostname()
    #     self.connection_ip_address = socket.gethostbyname(hostname)
    #     self.ip_address = f'{socket.gethostbyname(hostname)}:5000/'

    #     self.frames = []
    #     self.websites = []
        
    #     # subprocess.Popen(['python', 'remote_control/app.py'])
        
        
    #     db = get_database()
    #     cursor = db.cursor()
    #     query = "SELECT DISTINCT user_id FROM active_user_ip WHERE user_type = 'student' AND is_active = 12 AND connection_ip_address = %s;"
    #     values = (self.connection_ip_address,)
    #     cursor.execute(query, values)
    #     result = cursor.fetchall()

    #     keys = list(set(str(row[0]) for row in result))
    #     print("key: ", keys)
    #     num_subprocesses = len(keys)


    #     for i in range(num_subprocesses):
    #         subprocess.Popen(['python', 'remote_control/app.py'])
    #         self.websites.append(f'http://{self.ip_address}?key={keys[i]}')


    #     # for i in range(num_subprocesses):
    #     #     subprocess.Popen(['python', 'remote_control/app.py'])
            
    #     #     self.websites = [f'http://{self.ip_address}?key={key}' for key in keys]
    #     #     for website in self.websites:
    #     #         webbrowser.open(website)
    #     #         time.sleep(1)  # Add a delay of 1 second between opening websites


        
    #     self.timer_interval = 1000  
    #     self.update_query()

    #     # Set the number of frames per row
    #     frames_per_row = 3
    #     frame_count = 0
    #     if num_subprocesses:
    #         for website in self.websites:
    #             # create a new row if we've reached the maximum number of frames per row
    #             if frame_count % frames_per_row == 0:
    #                 row = len(self.frames) // frames_per_row
    #                 self.container_remote.grid_rowconfigure(row, weight=1)

    #             # create a new frame and add it to the current row
    #             self.frame = tkinterweb.HtmlFrame(
    #                 self.container_remote, width=5, height=5)
    #             self.frame.load_website(website)
    #             self.frame.grid(row=len(self.frames) // frames_per_row,
    #                             column=frame_count % frames_per_row, pady=10, padx=10, sticky="nsew")
    #             self.frames.append(self.frame)

    #             # create a new button and place it in the frame
    #             self.buttonMenu = customtkinter.CTkButton(
    #                 self.frame, text="⋮", font=("Arial", 30, 'bold'), width=2)
    #             self.buttonMenu.place(relx=1.0, x=-10, y=10, anchor="ne")

    #             # create a popup menu and add options
    #             self.popup_menu = tk.Menu(self.buttonMenu, tearoff=0)
    #             self.popup_menu.add_command(
    #                 label="View", command=lambda website=website: self.view_website(website))
    #             self.popup_menu.add_command(
    #                 label="Shutdown", command=self.shutdown)

    #             # bind the popup menu to the button
    #             def popup(event, popup_menu=self.popup_menu):
    #                 popup_menu.post(event.x_root, event.y_root)

    #             self.buttonMenu.bind("<Button-1>", popup)

    #             self.popup_menu.posted = False

    #             frame_count += 1

            
    #     # configure the columns to be evenly sized
    #     for i in range(frames_per_row):
    #         self.container_remote.grid_columnconfigure(i, weight=1)

    # def view_website(self, website):
    #     # Save the initial grid configuration
    #     self.initial_grid = [(frame.grid_info(), frame) for frame in self.frames]
        
    #     frames_per_row = 3
        
    #     # create a "go back" button to show all frames again
    #     self.go_back_button = customtkinter.CTkButton(
    #         self.container_remote, text="⬅ Go Back", font=("Arial", 16), command=self.show_all_frames)
    #     self.go_back_button.grid(
    #         row=len(self.frames) // 3 + 1, column=0, columnspan=frames_per_row, pady=10, sticky="ne")
    

    #     for frame in self.frames:
    #         # hide all frames except for the one with the selected website
    #         if frame.current_url != website:
    #             frame.grid_remove()
    #         else:
    #             # show the frame with the selected website
    #             frame.grid(row=10, column=0,  columnspan=frames_per_row, sticky="sew")



    # def show_all_frames(self):
    #     # Restore the initial grid configuration
    #     for grid_info, frame in self.initial_grid:
    #         frame.grid(**grid_info)

    #     self.go_back_button.destroy()
        
    # def on_close(self):
    #     subprocess.Popen(["pkill", "-9", "-f", "app.py"])
    #     # subprocess.call('taskkill /F /IM python.exe /T /FI "WINDOWTITLE eq app.py"', shell=True)

    # def shutdown(self):
    #     """Shutdown the remote access"""
        
    # def update_query(self):
    #     db = get_database()
    #     cursor = db.cursor()
    #     query = "SELECT DISTINCT user_id FROM active_user_ip WHERE user_type = 'student' AND is_active = 1 AND connection_ip_address = %s;"
    #     values = (self.connection_ip_address,)
    #     cursor.execute(query, values)
    #     result = cursor.fetchall()

    #     keys = list(set(str(row[0]) for row in result))
    #     print("key: ", keys)
    #     num_subprocesses = len(keys)



    #     # Check if there is a change in the data
    #     if num_subprocesses != len(self.websites):
    #         # Clear the current websites and update with the new data
    #         # self.websites = [f'http://{self.ip_address}?key={key}' for key in keys]
    #         # webbrowser.open(f'http://{self.ip_address}?key={key}' for key in keys)
    #         self.websites = [f'http://{self.ip_address}?key={key}' for key in keys]
    #         # for website in self.websites:
    #         #     webbrowser.open(website)

    #         # Refresh the frames with the updated websites
    #         self.refresh_frames(num_subprocesses)

    #     # Schedule the next update after 1 second
    #     self.container_remote.after(1000, self.update_query)

        
    # def refresh_frames(self, num_subprocesses):
    #     print('Updated')
    #     # Clear the current frames
    #     for frame in self.frames:
    #         frame.destroy()
    #     self.frames = []

    #     frames_per_row = 3
    #     frame_count = 0

    #     if num_subprocesses:
    #         for website in self.websites:
    #             # create a new row if we've reached the maximum number of frames per row
    #             if frame_count % frames_per_row == 0:
    #                 row = len(self.frames) // frames_per_row
    #                 self.container_remote.grid_rowconfigure(row, weight=1)

    #             # create a new frame and add it to the current row
    #             self.frame = tkinterweb.HtmlFrame(
    #                 self.container_remote, width=5, height=5)
    #             self.frame.load_website(website)
    #             self.frame.grid(row=len(self.frames) // frames_per_row,
    #                             column=frame_count % frames_per_row, pady=10, padx=10, sticky="nsew")
    #             self.frames.append(self.frame)

    #             # create a new button and place it in the frame
    #             self.buttonMenu = customtkinter.CTkButton(
    #                 self.frame, text="⋮", font=("Arial", 30, 'bold'), width=2)
    #             self.buttonMenu.place(relx=1.0, x=-10, y=10, anchor="ne")

    #             # create a popup menu and add options
    #             self.popup_menu = tk.Menu(self.buttonMenu, tearoff=0)
    #             self.popup_menu.add_command(
    #                 label="View", command=lambda website=website: self.view_website(website))
    #             # self.popup_menu.add_command(
    #             #     label="Shutdown", command=self.shutdown)

    #             # bind the popup menu to the button
    #             def popup(event, popup_menu=self.popup_menu):
    #                 popup_menu.post(event.x_root, event.y_root)

    #             self.buttonMenu.bind("<Button-1>", popup)

    #             self.popup_menu.posted = False

    #             frame_count += 1

    #     # configure the columns to be evenly sized
    #     for i in range(frames_per_row):
    #         self.container_remote.grid_columnconfigure(i, weight=1)
