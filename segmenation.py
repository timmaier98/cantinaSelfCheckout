import cv2
import numpy as np
import matplotlib.pyplot as plt

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
while True:
    succes, img = cap.read()
    if succes:
        img = cv2.resize(img, (1280, 720))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.GaussianBlur(img, (5, 5), 0)
        img = cv2.Canny(img, 100, 200)
        kernel = np.ones((5, 5))
        img = cv2.dilate(img, kernel, iterations=1)
        img = cv2.erode(img, kernel, iterations=1)
        contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 500:
                cv2.drawContours(img, cnt, -1, (255, 0, 0), 3)
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                x, y, w, h = cv2.boundingRect(approx)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                            (0, 255, 0), 2)
                cv2.putText(img, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                            (0, 255, 0), 2)
        cv2.imshow("Result", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break