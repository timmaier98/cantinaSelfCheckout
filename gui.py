import tkinter as tk
from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk
import cv2
import FPS as FPS

syscolor = "#031c29"
syscolorButtons = "#3a3a3a"
font_buttons = ("Calibri", 36)
custom_green = "#2FA572"
custom_red = "#A52F2F"

# Defines width  and height of the camera image
width = 1280
height = 720
frame_rate = 60


def gstreamer_pipeline(
    sensor_id=0,
    capture_width=width,
    capture_height=height,  
    display_width=width,
    display_height=height,
    framerate=frame_rate,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d !"
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink max-buffers=1 drop=true"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


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
        self.frame_base.pack(pady=10, padx=2, fill="both", expand=True)
        
        img_button = Image.open("./gui_images/confirmImage.png")
        img_button = img_button.resize((100, 100))
        photo_confirm_button = ImageTk.PhotoImage(img_button)
        
        btn = tk.Button(master=self.frame_base, image=photo_confirm_button, bg=syscolor, bd=0, activebackground=syscolor, highlightthickness=0)
        # btn = tk.Button(master=self.frame_base, text='Confirm', width=6, height=2, font=font_buttons, bg=custom_green, activebackground="red", borderwidth=10)
        btn.place(relx=0.99, rely=0.99, anchor=tk.SE)

        btnPics = tk.Button(master=self.frame_base, text='Take Pictures', width=6, height=2, font=font_buttons, bg=custom_green, activebackground="red", borderwidth=0)
        btnPics.place(relx=0.99, rely=0.1, anchor=tk.SE)
        # Video Elements
        self.cam = None
        self.cam_height = 680
        self.cam_width = int(self.cam_height*(14/9))
        self.cropdistX = 150
        self.cropdistY = 40
        self.image_label = tk.Label(self.frame_base, height=self.cam_height-2*self.cropdistY, width=self.cam_width-2*self.cropdistX, background=syscolor)
        self.image_label.place(relx=0.01, rely=0.01, anchor='nw')

        # self.start(cam_number="/dev/video3")
        self.start_csi()
        self.app.mainloop()

    def start(self, cam_number=0):
        """ Start the video feed with a given camera (0 is usually built-in webcam). """
        self.cam = cv2.VideoCapture(cam_number)
        self.cam.set(3, 1280)
        self.cam.set(4, 720)

        while True:
            ret, frame = self.cam.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (self.cam_width, self.cam_height))
                img_update = ImageTk.PhotoImage(Image.fromarray(frame))
                self.image_label.configure(image=img_update)
                self.image_label.update()
            else:
                print("Failed to grab frame from camera:", cam_number)

    def start_csi(self):
        fps_reader = FPS.FPS()
        # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
        print(gstreamer_pipeline(flip_method=0))
        video_capture = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)

        if video_capture.isOpened():
            try: 
                while True:
                    ret_val, frame = video_capture.read()       
                    if ret_val: 
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        frame = cv2.resize(frame, (self.cam_width, self.cam_height))
                        frame = frame[self.cropdistY:self.cam_height-self.cropdistY, self.cropdistX:self.cam_width-self.cropdistX]
                        fps, frame = fps_reader.update(img=frame)
                        img_update = ImageTk.PhotoImage(Image.fromarray(frame))
                        self.image_label.configure(image=img_update)
                        self.image_label.update()
                    else:
                        print("Failed to grab frame from CSI camera.")
            finally:
                video_capture.release()
                cv2.destroyAllWindows()
        else:
            print("Error: Unable to open camera")

    def stop(self):
        """ Stop the video feed and destroy all OpenCV windows. """
        self.cam.release()
        cv2.destroyAllWindows()
        print("Stopped!")


if __name__ == "__main__":
    gui = Gui()
