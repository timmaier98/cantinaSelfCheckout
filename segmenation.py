import os

import cv2
import numpy as np
import matplotlib.pyplot as plt
import gui_slider
import countour_detection

# cap = cv2.VideoCapture(2)
# use folder of images instead of webcam
# cap = cv2.VideoCapture("C:\\Users\\larsg\\CantinaSelfCheckoutDatasetMensa\\train\\NudelnBrokkoli/*.png")
# cap.set(3, 1280)
# cap.set(4, 720)

X_CROP = 70
Y_CROP = 200



gui_slider.create_gui()
path = "C:\\Users\\larsg\\CantinaSelfCheckoutDatasetMensa\\train"

class_dict = {}
# get classes from folder names
class_number = 0



for folder in os.listdir(path):
    # exclude files
    if "." not in folder:
        print("Now in Folder:", folder)
        class_dict[folder] = class_number
        print(class_dict)
        class_number += 1
        clas_folder = os.path.join(path, folder)
        j = 0
        for filename in os.listdir(clas_folder):
            # rename files into class name + number
            try:
                os.rename(os.path.join(clas_folder, filename), os.path.join(clas_folder, folder + str(j) + ".png"))
            except FileExistsError:
                pass
            j += 1
            print(filename)
            img = cv2.imread(os.path.join(clas_folder, filename))
            img_full = img.copy()
            IMAGE_WIDTH = img.shape[1]
            IMAGE_HEIGHT = img.shape[0]
            # crop 100 px from top bottom left and right
            img = img[X_CROP:-X_CROP, Y_CROP:-Y_CROP]
            img_original = img.copy()
            # if succes:
            radius_1, radius_2, cannyLow, cannyHigh, radius_5, radius_6, x_offset, y_offset = gui_slider.update_dart_trackbars()
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            for i in range(10):
                imgGray = cv2.GaussianBlur(img, (11, 11), 1)
            img = cv2.Canny(img, cannyLow, cannyHigh)
            cv2.imshow("Canny", img)
            kernel = np.ones((5, 5))
            img = cv2.dilate(img, kernel, iterations=1)
            img = cv2.erode(img, kernel, iterations=1)
            contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            # select the biggest contour
            contours = sorted(contours, key=cv2.contourArea, reverse=True)
            cnt = contours[0]
            area = cv2.contourArea(cnt)
            if area > radius_1 and area < radius_2*100:
                img = cv2.drawContours(img, cnt, -1, (255, 0, 0), 3)
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                x, y, w, h = cv2.boundingRect(approx)
                print(x, y, w, h)
                cv2.rectangle(img_original, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img_original, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                            (0, 255, 0), 2)
                cv2.putText(img_original, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                            (0, 255, 0), 2)
                # create a txt file with the same name as the image and write the coordinates of the bounding box in format x,y,w,h relative to the image size
                with open(os.path.join(path, filename[:-4] + ".txt"), "w") as f:
                    # remove offset from image
                    x = x + Y_CROP
                    y = y + X_CROP
                    scaled_X = x/IMAGE_WIDTH
                    scaled_Y = y/IMAGE_HEIGHT
                    scaled_W = w/IMAGE_WIDTH
                    scaled_H = h/IMAGE_HEIGHT
                    # cv2.rectangle(img_full, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    # cv2.imshow("full", cv2.resize(img_full, (0, 0), fx=0.5, fy=0.5))
                    # cv2.waitKey(1)
                    f.write(f"{class_dict[folder]} {scaled_X} {scaled_Y} {scaled_W} {scaled_H}")
                    f.close()

            cv2.imshow("Result", cv2.resize(img_original,(0, 0), fx=0.5, fy=0.5))
            # show images side by side

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

# create a yaml file with the following format:
# names:
# - Bier
# - Futter
# - Knoppers
# - Skittles
# - Snickers
# - Spezi
# nc: 6
# roboflow:
#   license: CC BY 4.0
#   project: ds2-szq20
#   url: https://universe.roboflow.com/ds2-z0dig/ds2-szq20/dataset/1
#   version: 1
#   workspace: ds2-z0dig
# test: ../test/images
# train: ds2-1/train/images
# val: ds2-1/valid/images

with open(os.path.join(path, "data.yaml"), "w") as f:
    f.write("names:\n")
    for key in class_dict:
        f.write(f"- {key}\n")
    f.write(f"nc: {len(class_dict)}\n")
    f.write("roboflow:\n")
    f.write("  license: CC BY 4.0\n")
    f.write("  project: ds2-szq20\n")
    f.write("  url: https://universe.roboflow.com/ds2-z0dig/ds2-szq20/dataset/1\n")
    f.write("  version: 1\n")
    f.write("  workspace: ds2-z0dig\n")
    f.write("test: ../test/images\n")
    f.write("train: ds2-1/train/images\n")
    f.write("val: ds2-1/valid/images\n")
    f.close()