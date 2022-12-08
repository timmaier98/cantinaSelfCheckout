import tkinter
import customtkinter as ctk


class Gui:
    def __init__(self):
        ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

        self.app = ctk.CTk()
        self.app.geometry("1024x600")
        self.app.resizable(False, False)
        self.app.title("cantinaSelfCheckout")

        frame_1 = ctk.CTkFrame(master=self.app)
        frame_1.pack(pady=20, padx=20, fill="both", expand=True)

        btn = ctk.CTkButton(master=self.app, text='huuh', anchor=tkinter.CENTER, width=400, height=100)
        btn.place(relx=0.5, rely=0.5)

        self.app.mainloop()


if __name__ == "__main__":
    gui = Gui()