# MIT License
# Copyright (c) 2019-2022 JetsonHacks

# Using a CSI camera (such as the Raspberry Pi Version 2) connected to a
# NVIDIA Jetson Nano Developer Kit using OpenCV
# Drivers for the camera and OpenCV are included in the base image

import cv2
#import undistort
import numpy as np
import sys
import FPS as FPS
import utils_own as utils
import gui_slider
import network
""" 
gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
Flip the image by setting the flip_method (most common values: 0 and 2)
display_width and display_height determine the size of each camera pane in the window on the screen
Default 1920x1080 displayd in a 1/4 size window
"""

#Defines width  and height of the camera image
width = 1920
height = 1080
frame_rate = 60

cap = cv2.VideoCapture(2)
cap.set(3, width)
cap.set(4, height)
# set frame rate
cap.set(cv2.CAP_PROP_FPS, frame_rate)

gui_slider.create_gui()

def main():
    window_title = "Webcam"
    # network.initialize_model("trained_models/own_data_with_none_class_fine_tuned.h5")
    network.initialize_model("Transfer_learning_CNNs/trained_models/mensa_esen16_12_2022_14_29_fine_tuned.h5")
    while 1:

        radius_1, radius_2, radius_3, radius_4, radius_5, radius_6, x_offset, y_offset = gui_slider.update_dart_trackbars()

        fpsreader = FPS.FPS()
        ret, frame = cap.read()
        fps, frame = fpsreader.update(img=frame)

        # detect circles in the image
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(image=gray, method=cv2.HOUGH_GRADIENT, dp=8, minDist=radius_1, minRadius=radius_2,
                                   maxRadius=radius_3, param1=radius_4, param2=radius_5)
        # ensure at least some circles were found
        if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")
            # loop over the (x, y) coordinates and radius of the circles
            for (x, y, r) in circles:
                # draw the circle in the output image, then draw a rectangle
                # corresponding to the center of the circle
                cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(frame, (x - r, y - r), (x + r, y + r), (0, 128, 255), 1)
                # cut out the rectangle
                cutout = frame[y - r:y + r, x - r:x + r]
                first_guess, predictions = network.evaluate_image(cutout)
                print(predictions)
                cv2.putText(frame, first_guess, (x - r, y - r), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


        cv2.imshow(window_title, utils.rez(frame,0.5))
        print(frame.shape)
        cv2.waitKey(1)

if __name__ == "__main__":
    print(cv2.__version__)
    main()
