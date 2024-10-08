import cv2
import numpy as np

'''
def empty(a):
    pass

cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640, 240)
cv2.createTrackbar("Hue Min", "TrackBars", 1, 179, empty)
cv2.createTrackbar("Hue Max", "TrackBars", 31, 179, empty)
cv2.createTrackbar("Sat Min", "TrackBars", 108, 255, empty)
cv2.createTrackbar("Sat Max", "TrackBars", 255, 255, empty)
cv2.createTrackbar("Val Min", "TrackBars", 0, 255, empty)
cv2.createTrackbar("Val Max", "TrackBars", 255, 255, empty)

'''

while True:
    '''
    h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    '''
    img = cv2.imread("Resources/uas takimages/5.png")
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    grassMask = cv2.inRange(imgHSV, np.array([36, 108, 0]), np.array([117, 255, 255]))
    g_mask_bgr = cv2.cvtColor(grassMask, cv2.COLOR_GRAY2BGR)
    cyanMask = np.zeros_like(g_mask_bgr)
    cyanMask[:] = [251, 252, 102]
    GrassMaskResult = cv2.bitwise_and(cyanMask, g_mask_bgr, mask=grassMask)

    burntMask = cv2.inRange(imgHSV, np.array([1, 108, 0]), np.array([36, 255, 255]))
    mask_bgr = cv2.cvtColor(burntMask, cv2.COLOR_GRAY2BGR)
    yellowMask = np.zeros_like(mask_bgr)
    yellowMask[:] = [102, 252, 252]
    burntMaskResult = cv2.bitwise_and(yellowMask, mask_bgr, mask=burntMask)

    i_trianglesMask = cv2.inRange(imgHSV, np.array([1, 108, 0]), np.array([117, 255, 255]))
    trianglesMask = cv2.bitwise_not(i_trianglesMask)
    t_imgResult = cv2.bitwise_and(img, img, mask=trianglesMask)

    imgResult = cv2.bitwise_or(GrassMaskResult, burntMaskResult)
    imgResult = cv2.bitwise_or(imgResult, t_imgResult)

    # cv2.imshow("original", img)
    # cv2.imshow("HSV", imgHSV)
    # cv2.imshow("Mask", trianglesMask)
    cv2.imshow("ImageResult", imgResult)
    cv2.waitKey(1)