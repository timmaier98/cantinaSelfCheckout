import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from PIL import Image, ImageTk
import cv2
import FPS as FPS
import torch
from prices import prices
syscolor = "#031c29"
syscolorButtons = "#3a3a3a"
font_buttons = ("Calibri", 16)
custom_green = "#2FA572"
custom_green_pressed = "#106A43"
custom_orange = "#e67627"
custom_orange_pressed = "#c26421"
custom_red = "#A52F2F"

# Defines width  and height of the camera image
width = 1280
height = 720
frame_rate = 60

print("Starting GUI.py")
print("loading model")
model = torch.hub.load("ultralytics/yolov5", "custom",
                      path="/media/jetson/KINGSTON/cantinaSelfCheckout/Yolo/yolov5/trained_models/best.pt",
                      force_reload=False)
print("done loading model")


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
        # self.app.attributes("-fullscreen", True)

        self.app.bind("<Escape>", lambda e: self.app.destroy())
        self.app.bind("<s>", self.take_sample_pictures)

        s = ttk.Style()
        s.configure('Custom.TFrame', background=syscolor)

        self.path = "/media/jetson/KINGSTON/cantinaSelfCheckout/Trainingsbilder/newMeal"

        self.frame_base = ttk.Frame(master=self.app, style='Custom.TFrame')
        self.frame_base.pack(pady=10, padx=2, fill="both", expand=True)
        self.overall_price = 0

        confirm_img = Image.open("./gui_images/confirmImage.png")
        confirm_img = confirm_img.resize((100, 100))
        photo_confirm_button = ImageTk.PhotoImage(confirm_img)
        confirm_button = tk.Button(master=self.frame_base, image=photo_confirm_button, bg=syscolor, bd=0, activebackground=syscolor, highlightthickness=0)
        confirm_button.place(relx=0.99, rely=0.99, anchor=tk.SE)

        repeat_img = Image.open("./gui_images/repeat.png")
        repeat_img = repeat_img.resize((105, 105))
        photo_repeat_button = ImageTk.PhotoImage(repeat_img)
        repeat_button = tk.Button(master=self.frame_base, image=photo_repeat_button, bg=syscolor, bd=0, activebackground=syscolor, highlightthickness=0)
        repeat_button.place(relx=0.87, rely=0.99, anchor=tk.SE)

        btn_pics = tk.Button(master=self.frame_base, text='Choose directory', width=12, height=1, font=font_buttons, bg=custom_orange,
                            activebackground=custom_orange_pressed, borderwidth=0, command=self.choose_directory)
        btn_pics.place(relx=0.97, rely=0.02, anchor=tk.NE)
        
        self.dirVar = StringVar()
        self.dirVar.set("cantinaSelfCheckout/Trainingsbilder/newMeal")
        dir_text_box = tk.Label(master=self.frame_base, textvariable=self.dirVar, font=("Calibri", 10), bg=syscolor, foreground="white", width=25)
        dir_text_box.place(relx=0.97, rely=0.1, anchor=tk.NE)

        self.listbox = Listbox(self.frame_base, width=22, height=10, bg=syscolor, fg="white")  
        self.listbox.place(relx=0.97, rely=0.2, anchor=tk.NE)

        self.dirVarMoney = StringVar()
        self.dirVarMoney.set("0 €")
        dir_text_box_price = tk.Label(master=self.frame_base, textvariable=self.dirVarMoney, font=("Calibri", 10), bg=syscolor, foreground="white", width=25)
        dir_text_box_price.place(relx=0.97, rely=0.6, anchor=tk.NE)
        
        # Video Elements
        self.cam = None
        self.cam_height = 680
        self.cam_width = int(self.cam_height*(14/9))
        self.cropdistX = 150
        self.cropdistY = 40
        self.image_label = tk.Label(self.frame_base, height=self.cam_height-2*self.cropdistY, width=self.cam_width-2*self.cropdistX, background=syscolor)
        self.image_label.place(relx=0.01, rely=0.01, anchor='nw')
        self.globalFrame = None
        self.index = 0

        # self.start(cam_number="/dev/video3")
        self.start_csi()
        self.app.mainloop()
    
    def take_sample_pictures(self, *event):
        print('Saving Frame')
        cv2.imwrite(self.path + "/c" +str(self.index)+'.png', self.globalFrame)
        self.index += 1

    def choose_directory(self):
        self.index = 0 
        path = filedialog.askdirectory(initialdir="/home/jetson/desktop/cantinaSelfCheckout", title="Choose a directory")
        self.path = path
        path = path[20:]
        self.dirVar.set(path)
        print(self.dirVar)

    def start(self, cam_number=0):
        """ Start the video feed with a given camera (0 is usually built-in webcam). """
        self.cam = cv2.VideoCapture(cam_number)
        self.cam.set(3, 1280)
        self.cam.set(4, 720)

        fps_reader = FPS.FPS()
        while True:
            ret, frame = self.cam.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (self.cam_width, self.cam_height))
                frame = frame[self.cropdistY:self.cam_height - self.cropdistY, self.cropdistX:self.cam_width - self.cropdistX]
                self.globalFrame = frame
                fps, frame = fps_reader.update(img=frame)
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
                        self.globalFrame = frame
                        results = model(frame)
                        results.print()
                        df = results.pandas().xyxy[0]
                        sum_price = self.calculate_overall_price(df)
                        print(sum_price)
                        frame_w_bb = results.render()
                        frame = frame_w_bb[0]
                        fps, frame = fps_reader.update(img=frame)
                        img_update = ImageTk.PhotoImage(Image.fromarray(frame))
                        self.image_label.configure(image=img_update)
                        self.image_label.update()
                        self.listbox.delete(0, self.listbox.size())
                        self.dirVarMoney.set(f"{sum_price} €")
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

    def calculate_overall_price(self, df):
        total_price = 0
        # get the price of each item in the df with the name col
        df['price'] = df['name'].apply(lambda x: prices[x])

        # check if df contains item with name 'AtheneKarte':
        multiplier = 1
        student_multiplier = 0.8
        if 'AtheneKarte' in df['name'].values:
            multiplier = student_multiplier
            # remove the AtheneKarte from the df
            df = df[df['name'] != 'AtheneKarte']
            self.listbox.insert(0, "Student-Discount applied!")

        # sort dataframe alphabetically:
        df = df.sort_values(by=['name'])
        for index, row in df.iterrows():
            if multiplier == student_multiplier:
                index += 1
            item_price = row['price'] * multiplier
            item_price = round(item_price, 2)
            total_price += item_price
            self.listbox.insert(index,f"{row['name']} {item_price}€")
        return total_price


if __name__ == "__main__":
    gui = Gui()
