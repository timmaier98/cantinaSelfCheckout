import cv2


cam  = cv2.VideoCapture("/dev/video0")

while 1:
    ret , frame = cam.read()
    if ret:
        cv2.imshow("Name",frame)
        cv2.waitKey(1)
    else:
        print("No Frame")
