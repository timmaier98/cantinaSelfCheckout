import tkinter as tk
from tkinter import *
from tkinter import ttk

class Gui:

    def __init__(self):

        syscolor = "#031c29"
        syscolorButtons = "#3a3a3a"
        Font_Buttons = ("Roboto", 36)
        custom_green = "#2FA572"
        custom_red = "#A52F2F"

        #tk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
        #tk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

        self.app = tk.Tk()
        self.app.geometry("1024x600")
        self.app.resizable(False, False)
        self.app.title("cantinaSelfCheckout")
        self.app.config(background=syscolor)  # Hintergrundfarbe des Fensters

        s = ttk.Style()
        s.configure('Custom.TFrame', background=syscolor)

        self.frame_base = ttk.Frame(master=self.app, style='Custom.TFrame')
        self.frame_base.pack(pady=20, padx=20, fill="both", expand=True)

        btn = tk.Button(master=self.frame_base, text='Confirm', width=8, height=2,
                         font=Font_Buttons)
        btn.place(relx=0.99, rely=0.99, anchor=tk.SE)

        self.app.mainloop()


if __name__ == "__main__":
    gui = Gui()