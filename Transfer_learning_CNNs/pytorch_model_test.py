import torch
import cv2

# Load the model from pt file
model = torch.load("C:\\Users\\larsg\\PycharmProjects\\cantinaSelfCheckout\\Yolo\\runs_Tim\\train\\exp4\\weights\\best.pt")
model.load_state_dict(torch.load('model_weights.pth'))
cap = cv2.VideoCapture(2)
cap.set(3, 1280)
cap.set(4, 720)

while True:
    success, img = cap.read()
    if success:
        cv2.imshow("Image", img)
        # use the model to predict the image
        results = model(img)
        results.print()  # or .show(), .save()        cv2.waitKey(1)
