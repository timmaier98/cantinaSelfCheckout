import yolov7
import time
import os
import cv2


weights = "C:\\Users\\Lars\\PycharmProjects\\cantinaSelfCheckout\\Yolo\\yolov7\\weights\\yolov7_weights.pt"

model = yolov7.load(weights, trace=True, size=640)


# set model parameters
model.conf = 0.25  # NMS confidence threshold
model.iou = 0.45  # NMS IoU threshold
model.classes = None  # (optional list) filter by class

# set image
img = 'C:\\Users\\Lars\\PycharmProjects\\cantinaSelfCheckout\\Yolo\\yolov7\\test_imgs\\IMG_1116.JPG'

path = 'C:\\Users\\Lars\\PycharmProjects\\cantinaSelfCheckout\\Yolo\\yolov7\\test_imgs'
# perform inference
for file in os.listdir(path):
    if file.endswith(".jpg"):
        path_to_img = os.path.join(path, file)
        start = time.time()
        results = model(path_to_img)
        end = time.time()
        # print(end - start)
        results.print()
        results.render()
        cv2.imshow("Image", cv2.cvtColor(cv2.resize(results.imgs[0], (640, 480)), cv2.COLOR_RGB2BGR))
        cv2.waitKey(1)



# # parse results
# predictions = results.pred[0]
# boxes = predictions[:, :4] # x1, y1, x2, y2
# scores = predictions[:, 4]
# categories = predictions[:, 5]
#
# # show detection bounding boxes on image
# results.show()