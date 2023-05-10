import tkinter
import tkinter.messagebox
import customtkinter

# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("System")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{500}x{500}")  # smaller size

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create appearance mode label and option menu

        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(
            row=0, column=2, padx=(0, 20), sticky="w")

        # create login system
        self.login_label = customtkinter.CTkLabel(
            self, text="Login System", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.login_label.grid(row=1, column=1, columnspan=2,
                              pady=(30, 10), sticky="nsew")

        self.email_label = customtkinter.CTkLabel(
            self, text="Email/Username:", anchor="w")
        self.email_label.grid(row=2, column=1, padx=(
            20, 0), pady=(20, 0), sticky="w")

        self.email_entry = customtkinter.CTkEntry(self)
        self.email_entry.grid(row=3, column=1, columnspan=2, padx=(
            20, 20), pady=(0, 20), sticky="nsew")

        self.password_label = customtkinter.CTkLabel(
            self, text="Password:", anchor="w")
        self.password_label.grid(row=4, column=1, padx=(
            20, 0), pady=(0, 0), sticky="w")

        self.password_entry = customtkinter.CTkEntry(
            self, show="*")
        self.password_entry.grid(row=5, column=1, columnspan=2, padx=(
            20, 20), pady=(0, 20), sticky="nsew")

        self.login_button = customtkinter.CTkButton(
            self, text="Login", fg_color="blue", command=self.login_event)
        self.login_button.grid(row=6, column=1, columnspan=2,
                               padx=(20, 20), pady=(10, 20), sticky="nsew")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def login_event(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        combobox_value = self.combobox.get()
        tkinter.messagebox.showinfo(
            "Login Info", f"Email: {email}, Password: {password}, ComboBox Value: {combobox_value}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
