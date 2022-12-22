import torch
import cv2
#
# # Load the model from pt file
# # model = torch.hub.load("ultralytics/yolov5", "custom", path="trained_models/yolov5s.pt")
# # model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)
# model = torch.hub.load("yolov5/torch/hub/ultralytics_yolov5_master", "custom",
#                        path="C:\\Users\\larsg\\PycharmProjects\\cantinaSelfCheckout\\Yolo\\runs_Tim\\train\\exp6\\weights\\best.pt", source="local")
# # model = torch.hub.load(".", "custom", path="C:\\Users\\larsg\\PycharmProjects\\cantinaSelfCheckout\\Yolo\\runs_Tim\\train\\exp6\\weights\\best.pt", source="local")
# # load the weights from the trained model
# # model.load_state_dict(torch.load("trained_models/yolov5s.pt", map_location=torch.device('cpu'))['model'].float().state_dict(), strict=False)
# # model.load_state_dict(torch.load('C:\\Users\\larsg\\PycharmProjects\\cantinaSelfCheckout\\Yolo\\runs_Tim\\train\\exp5\\weights\\best.pt'))
cap = cv2.VideoCapture(2)
cap.set(3, 1280)
cap.set(4, 720)

model = torch.hub.load("ultralytics/yolov5", "custom",
                       path="C:\\Users\\larsg\\PycharmProjects\\cantinaSelfCheckout\\Yolo\\trained_models\\model_- 16 december 2022 23_16.pt",
                       force_reload=False)
while True:
    success, img = cap.read()
    if success:
        # use the model to predict the image
        results = model(img)
        results.print()  # or .show(), .save()        cv2.waitKey(1)
        # put results on image
        results.render()
        cv2.imshow("Image", img)
        cv2.waitKey(1)



