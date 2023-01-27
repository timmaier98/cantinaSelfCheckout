import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from PIL import Image, ImageTk
import cv2
import FPS as FPS
import torch
from prices import prices
import pandas as pd
import numpy as np
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

loadModel = True
contDetection = True
devMode = False
tensorrt = False

PATH = "/home/jetson/cantinaSelfCheckout/"

print("Starting GUI.py")
print("loading model")
if loadModel:
  # if tensorrt:
  #      from models.common import DetectMultiBackend
  #      tensor_rt_engine_path = PATH + "Yolo/yolov8/yolov8.engine"
  #
  #       device = torch.device(0)
  #       model = DetectMultiBackend(tensor_rt_engine_path, device=device,
  #                              # dnn=dnn,
  #                               # data=data,
  #                               fp16=True
  #                              )
  #     model.eval()
  #     model.cuda()
    model = torch.hub.load("ultralytics/yolov5", "custom",
                           path=f"{PATH}Yolo/yolov5/trained_models/best_new_classes.pt",
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
        self.app.attributes("-fullscreen", True)

        self.app.bind("<Escape>", lambda e: self.app.destroy())
        self.app.bind("<s>", self.take_sample_pictures)

        s = ttk.Style()
        s.configure('Custom.TFrame', background=syscolor)
        
        self.frame_base = ttk.Frame(master=self.app, style='Custom.TFrame')
        self.frame_base.pack(pady=10, padx=2, fill="both", expand=True)
        self.overall_price = 0

        self.df_list = [pd.DataFrame() for i in range(5)]
        self.stop_detecting = False
        self.start_detecting = True

        if devMode:
            self.path = f"{PATH}Trainingsbilder/newMeal"
            btn_pics = tk.Button(master=self.frame_base, text='Choose directory', width=12, height=1, font=font_buttons, bg=custom_orange,
                            activebackground=custom_orange_pressed, borderwidth=0, command=self.choose_directory)
            btn_pics.place(relx=0.97, rely=0.02, anchor=tk.NE)
           
            self.dirVar = StringVar()
            self.dirVar.set("cantinaSelfCheckout/Trainingsbilder/newMeal")
            dir_text_box = tk.Label(master=self.frame_base, textvariable=self.dirVar, font=("Calibri", 10), bg=syscolor, foreground="white", width=25)
            dir_text_box.place(relx=0.97, rely=0.1, anchor=tk.NE)
        else:
            logo_img = Image.open("./gui_images/logo_final_weiss.png")
            logo_img = logo_img.resize((int(180), 180))
            photo_logo = ImageTk.PhotoImage(logo_img)
            logo_lable = tk.Label(master=self.frame_base, image=photo_logo, bg=syscolor)
            logo_lable.place(relx=0.97, rely=-0.02, anchor=tk.NE)            


        self.btn_pics = tk.Button(master=self.frame_base, text='Choose manually', width=12, height=1, font=font_buttons, bg=custom_orange,
                            activebackground=custom_orange_pressed, borderwidth=0, command=self.close)

        confirm_img = Image.open("./gui_images/confirmImage.png")
        confirm_img = confirm_img.resize((100, 100))
        photo_confirm_button = ImageTk.PhotoImage(confirm_img)
        confirm_button = tk.Button(master=self.frame_base, image=photo_confirm_button, bg=syscolor, bd=0, activebackground=syscolor, highlightthickness=0, command=self.confirm_pressed)
        confirm_button.place(relx=0.99, rely=0.99, anchor=tk.SE)

        repeat_img = Image.open("./gui_images/repeat.png")
        repeat_img = repeat_img.resize((105, 105))
        photo_repeat_button = ImageTk.PhotoImage(repeat_img)
        repeat_button = tk.Button(master=self.frame_base, image=photo_repeat_button, bg=syscolor, bd=0, activebackground=syscolor, highlightthickness=0, command=self.repeat_pressed)
        repeat_button.place(relx=0.87, rely=0.99, anchor=tk.SE)

        self.listbox = Listbox(self.frame_base, width=22, height=10, bg=syscolor, fg="white")  
        self.listbox.place(relx=0.97, rely=0.3, anchor=tk.NE)
        detected_meals_lable = tk.Label(master=self.frame_base, text="Detected meals:", font=("Calibri", 16), bg=syscolor, foreground="white", width=25)
        detected_meals_lable.place(relx=0.72, rely=0.25, anchor=tk.NW)

        self.dirVarMoney = StringVar()
        self.dirVarMoney.set("Total: 0.00 €")
        dir_text_box_price = tk.Label(master=self.frame_base, textvariable=self.dirVarMoney, font=("Calibri", 20), bg=syscolor, foreground="white", width=25)
        dir_text_box_price.place(relx=0.683, rely=0.62, anchor=tk.NW)
        self.student_discount_lable = tk.Label(master=self.frame_base, text="Student-Discount applied!", font=("Calibri", 10), bg=syscolor, foreground="#00A912", width=25)

        
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
        self.globalFrame = cv2.cvtColor(self.globalFrame, cv2.COLOR_RGB2BGR)
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
        detecting_string = "Detecting"

        if video_capture.isOpened():
            try: 
                while True:
                    ret_val, frame = video_capture.read()     
                    if ret_val: 
                        if not self.stop_detecting:
                            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            frame = cv2.resize(frame, (self.cam_width, self.cam_height))
                            frame = frame[self.cropdistY:self.cam_height-self.cropdistY, self.cropdistX:self.cam_width-self.cropdistX]
                            self.globalFrame = frame.copy()
                            if loadModel:
                                if tensorrt:
                                    frame_model = frame.copy()
                                    frame_model = cv2.resize(frame_model, (640,640))
                                    frame_model = np.transpose(frame_model, (2,0,1))
                                    frame_model = np.expand_dims(frame_model, 0)
                                    results = model(frame_model)
                                    self.postprocess(results)
                                else:
                                    results = model(frame)
                                    results.print()
                                
                                df = results.pandas().xyxy[0]
                                df = df.sort_values('name')
                                df = df.reset_index(drop = True)
                                sum_price = self.calculate_overall_price(df)
                                print(df)
                                if not df.empty:
                                      self.df_list.append(df["name"])
                                      self.df_list.pop(0)
                                      if self.check_if_df_are_equal(self.df_list) and self.start_detecting:
                                          self.stop_detecting = True
                                          self.start_detecting = False
                                          self.df_list = [pd.DataFrame() for i in range(5)]
                                else: 
                                      self.start_detecting = True
                                      self.df_list = [pd.DataFrame() for i in range(5)]
                                frame_w_bb = results.render()
                                frame = frame_w_bb[0]
                                
                            fps, frame = fps_reader.update(img=frame)
                            if self.stop_detecting:
                                frame = cv2.putText(frame, "Detected", (frame.shape[0] - 40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            else:
                                frame = cv2.putText(frame, detecting_string, (frame.shape[0] - 40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                                detecting_string += "."
                                if len(detecting_string) >= 13:
                                    detecting_string = "Detecting"
                            img_update = ImageTk.PhotoImage(Image.fromarray(frame))
                            self.image_label.configure(image=img_update)
                            self.image_label.update()
                            if loadModel and not self.stop_detecting:
                                self.listbox.delete(0, self.listbox.size())
                                self.dirVarMoney.set(f"Total: {sum_price:.2f} €")
                        else: 
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
    def close(self):
        self.app.destroy()


    def postprocess(self, output_data):
         # get class names
        with open("classes.txt") as f:
            classes = [line.strip() for line in f.readlines()]
        # calculate human-readable value by softmax
        confidences = torch.nn.functional.softmax(output_data, dim=1)[0] * 100
        print("confinences", confidences)
        # find top predicted classes
        _, indices = torch.sort(output_data, descending=True)
        print("indices", indices)
        i = 0
        # print the top classes predicted by the model
        while confidences[indices[0][i]] > 0.5:
            class_idx = indices[0][i]
            print(
	    "class:",
	    classes[class_idx],
	    ", confidence:",
	    confidences[class_idx].item(),
	    "%, index:",
	    class_idx.item(),
            )
            i += 1

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
            self.student_discount_lable.place(relx=0.782, rely=0.59, anchor=tk.NW)
        else: 
            self.student_discount_lable.place_forget()

        # sort dataframe alphabetically:
        for index, row in df.iterrows():
            item_price = row['price'] * multiplier
            item_price = round(item_price, 2)
            total_price += item_price
            if row['name'] == "Futter":
               row['name'] = "Studentenfutter"
            self.listbox.insert(index,f"{row['name']} {item_price:.2f}€")
        total_price = round(total_price, 2)
        return total_price

    def check_if_df_are_equal(self, df_list):
        for df in df_list:
            if not df_list[0].equals(df):
                return False
        return True

    def confirm_pressed(self):
        self.stop_detecting = False
        self.btn_pics.place_forget()
        self.listbox.delete(0, self.listbox.size())
        self.dirVarMoney.set(f"Total: 0.00 €")
        self.df_list = [pd.DataFrame() for i in range(5)]

    def repeat_pressed(self):
        self.stop_detecting = False
        self.btn_pics.place(relx=0.97, rely=0.72, anchor=tk.NE)
        self.listbox.delete(0, self.listbox.size())
        self.dirVarMoney.set(f"Total: 0.00 €")
        self.df_list = [pd.DataFrame() for i in range(5)]
        self.start_detecting = True

if __name__ == "__main__":
    gui = Gui()
