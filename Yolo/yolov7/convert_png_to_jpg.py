# convert every png file in the current directory to jpg
import os
import cv2

path = "C:\\Users\\Lars\\PycharmProjects\\cantinaSelfCheckout\\Yolo\\yolov7\\test_imgs"

for file in os.listdir(path):
    if file.endswith(".png"):
        img = cv2.imread(os.path.join(path, file))
        cv2.imwrite(os.path.join(path, file.replace(".png", ".jpg")), img)
        os.remove(os.path.join(path, file))
