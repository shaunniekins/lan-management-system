# importing required modules
import tkinter
import customtkinter
from PIL import ImageTk, Image

# Modes: system (default), light, dark
customtkinter.set_appearance_mode("system")
# Themes: blue (default), dark-blue, green
customtkinter.set_default_color_theme("green")


class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):  # added missing arguments
        super().__init__(*args, **kwargs)

        self.geometry("600x440")  # replaced app with self
        self.title('Login')

        self.img1 = ImageTk.PhotoImage(Image.open("pattern.png"))
        self.l1 = customtkinter.CTkLabel(master=self, image=self.img1)
        self.l1.pack()

        # creating custom frame
        self.frame = customtkinter.CTkFrame(
            master=self.l1, width=320, height=360, corner_radius=15)
        self.frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.l2 = customtkinter.CTkLabel(
            master=self.frame, text="Log into your Account", font=('Century Gothic', 20))
        self.l2.place(x=50, y=45)

        self.entry1 = customtkinter.CTkEntry(
            master=self.frame, width=220)
        self.entry1.place(x=50, y=110)

        self.entry2 = customtkinter.CTkEntry(
            master=self.frame, width=220, show="*")
        self.entry2.place(x=50, y=165)

        self.l3 = customtkinter.CTkLabel(
            master=self.frame, text="Forget password?", font=('Century Gothic', 12))
        self.l3.place(x=155, y=195)

        # Create custom button
        self.button1 = customtkinter.CTkButton(
            master=self.frame, width=220, text="Login", command=self.button_function, corner_radius=6)
        self.button1.place(x=50, y=240)

    def button_function(self):  # added missing self argument
        self.destroy()  # replaced app with self
        w = customtkinter.CTk()
        w.geometry("1280x720")
        w.title('Welcome')
        l1 = customtkinter.CTkLabel(
            master=w, text="Home Page", font=('Century Gothic', 60))
        l1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        w.mainloop()


if __name__ == "__main__":
    app = App()
    app.mainloop()
