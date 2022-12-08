import tkinter as tk
from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk
import cv2

syscolor = "#031c29"
syscolorButtons = "#3a3a3a"
font_buttons = ("Calibri", 36)
custom_green = "#2FA572"
custom_red = "#A52F2F"


class Gui:
    def __init__(self):
        self.app = tk.Tk()
        self.app.geometry("1024x600")
        # self.app.resizable(False, False)
        self.app.title("cantinaSelfCheckout")
        self.app.config(background=syscolor)  # background color of the window
        self.app.attributes("-fullscreen", True)

        self.app.bind("<Escape>", lambda e: self.app.destroy())

        s = ttk.Style()
        s.configure('Custom.TFrame', background=syscolor)

        self.frame_base = ttk.Frame(master=self.app, style='Custom.TFrame')
        self.frame_base.pack(pady=20, padx=20, fill="both", expand=True)

        btn = tk.Button(master=self.frame_base, text='Confirm', width=6, height=2, font=font_buttons, bg=custom_green)
        btn.place(relx=0.99, rely=0.99, anchor=tk.SE)

        # Video Elements
        self.cam = None
        self.cam_height = 680
        self.cam_width = 700
        self.image_label = tk.Label(self.frame_base, height=self.cam_height, width=self.cam_width, background="red")
        self.image_label.place(relx=0.01, rely=0.01, anchor='nw')

        # start_btn = tk.Button(self.app, text="Start", command=self.start, height=5, width=8)
        # start_btn.place(relx=0.99, rely=0.3, anchor='se')
        # stop_btn = tk.Button(master=self.frame_base, text='Stop', width=8, height=2, font=font_buttons, command=self.stop)
        # stop_btn.place(relx=0.99, rely=0.5, anchor='se')

        self.start(cam_number = 0)
        self.app.mainloop()

    def start(self, cam_number=0):
        """ Start the video feed with a given camera (0 is usually built-in webcam). """
        #self.cam = cv2.VideoCapture(0)
        self.cam = cv2.VideoCapture("/dev/video3")
        self.cam.set(3, 1280)
        self.cam.set(4, 720)

        while True:
            ret, frame = self.cam.read()

            if not ret:
                print("Failed to grab frame from camera:", cam_number)
                # break
            else:
                # Update the image to tkinter...
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (self.cam_width, self.cam_height))
                img_update = ImageTk.PhotoImage(Image.fromarray(frame))
                self.image_label.configure(image=img_update)
                self.image_label.update()

    def stop(self):
        """ Stop the video feed and destroy all windows. """
        self.cam.release()
        cv2.destroyAllWindows()
        print("Stopped!")


if __name__ == "__main__":
    gui = Gui()
