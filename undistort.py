import numpy as np
import sys
import cv2
# You should replace these 3 lines with the output in calibration step
DIM=(1920, 1080)
K=np.array([[999.4120038145531, 0.0, 948.6842036405939], [0.0, 999.0435340621482, 555.6832121924273], [0.0, 0.0, 1.0]])
D=np.array([[-0.027935046924675477], [-0.008674900572807258], [0.008503665011061427], [-0.00495484091780125]])
img = cv2.imread('c1.png')

with open('map1_map2.npy','rb') as f:
     map1 = np.load(f)
     map2 = np.load(f)

def undistort(img, balance=0.0, dim2=None, dim3=None):
    # dim1 = img.shape[:2][::-1]  #dim1 is the dimension of input image to un-distort
    # assert dim1[0]/dim1[1] == DIM[0]/DIM[1], "Image to undistort needs to have same aspect ratio as the ones used in calibration"
    # if not dim2:
    #     dim2 = dim1
    # if not dim3:
    #     dim3 = dim1
    # scaled_K = K * dim1[0] / DIM[0]  # The values of K is to scale with image dimension.
    # scaled_K[2][2] = 1.0  # Except that K[2][2] is always 1.0
    # This is how scaled_K, dim2 and balance are used to determine the final K used to un-distort image. OpenCV document failed to make this clear!
    
    # new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(scaled_K, D, dim2, np.eye(3), balance=balance)
    # map1, map2 = cv2.fisheye.initUndistortRectifyMap(scaled_K, D, np.eye(3), new_K, dim3, cv2.CV_16SC2)
    # with open('map1.npy','wb') as f:
    #     np.save(f,map1)
    #     np.save(f,map2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    return undistorted_img

undistort(img)