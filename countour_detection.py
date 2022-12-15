import cv2
import numpy as np


def get_contours(img, shapeROI = 0, cThr=[100, 150], gaussFilters = 1,dialations = 1,errsoions = 1, showFilters=False, minArea=500, epsilon = 0.01, Cornerfilter=0, draw=False):
    """
    gets Contours from an image

    :param img: input image (numpy array)
    :param cThr: thrersholds for canny edge detector (list)
    :param gaussFilters: number of gaussian smoothing filters (int)
    :param showFilters: boolean if you want to see the filters
    :param minArea: minimum area of vontours to filter out small noise
    :param epsilon: 'resolution' of polynomial approximation of the contour
    :param Cornerfilter: Only outputs contours with n corners
    :param draw: draws detected contours on img
    :return: image with contours on it, (length of contour, area of contour, poly approximation, boundingbox to the contour, i)
    """
    minArea = minArea/1000   #HIGHLIGHT: Only for very small resolution testing
    imgContours = img
    #imgContours = cv2.UMat(img)
    imgGray = cv2.cvtColor(imgContours, cv2.COLOR_BGR2GRAY)
    for i in range(gaussFilters):
       imgGray = cv2.GaussianBlur(imgGray, (11, 11),1)
    if showFilters: cv2.imshow("Gauss",cv2.resize(imgGray, (int(shapeROI[1]),int(shapeROI[0])), interpolation=cv2.INTER_AREA))
    imgCanny = cv2.Canny(imgGray, cThr[0], cThr[1])
    kernel = np.ones((3, 3))
    imgDial = cv2.dilate(imgCanny, kernel, iterations=dialations)
    imgThre = cv2.erode(imgDial, kernel, iterations=errsoions)
    if showFilters: cv2.imshow('Canny',cv2.resize(imgThre, (int(shapeROI[1]),int(shapeROI[0])), interpolation=cv2.INTER_AREA))
    contours, hiearchy = cv2.findContours(imgThre, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    finalCountours = []
    for i in contours:
        area = cv2.contourArea(i)
        if area > minArea:
            #print('minAreaFilled')
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, epsilon * peri, True)
            bbox = cv2.boundingRect(approx)
            if Cornerfilter > 0:
                if len(approx) == Cornerfilter:
                    finalCountours.append([len(approx), area, approx, bbox, i])
            else:
                finalCountours.append([len(approx), area, approx, bbox, i])
    finalCountours = sorted(finalCountours, key=lambda x: x[1], reverse=True)

    if draw:
        for con in finalCountours:
            cv2.drawContours(imgContours, con[4], -1, (0, 0, 255), 3)

    # if not showFilters:
    #     cv2.destroyWindow("Gauss")
    #     cv2.destroyWindow("Canny")
    return imgContours, finalCountours