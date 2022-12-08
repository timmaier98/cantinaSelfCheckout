import tkinter
import customtkinter as ctk


class Gui:

    def __init__(self):

        Font_Buttons = ("Roman", 36)
        custom_green = "#2FA572"
        custom_red = "#A52F2F"

        ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

        self.app = ctk.CTk()
        self.app.geometry("1024x600")
        self.app.resizable(False, False)
        self.app.title("cantinaSelfCheckout")

        self.frame_base = ctk.CTkFrame(master=self.app)
        self.frame_base.pack(pady=20, padx=20, fill="both", expand=True)

        btn = ctk.CTkButton(master=self.frame_base, text='Confirm', width=200, height=100, text_color="white",
                            font=Font_Buttons, fg_color=custom_green)
        btn.place(relx=0.99, rely=0.99, anchor=tkinter.SE)

        self.app.mainloop()


if __name__ == "__main__":
    gui = Gui()