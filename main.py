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
def GetVerticesAmount(img):
    imgBlur = cv2.GaussianBlur(img, (7, 7), 1)
    imgCanny = cv2.Canny(imgBlur, 500, 500)
    contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    triangleCount = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            # cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            objCord = len(approx)
            if objCord == 3:
                triangleCount += 1
    return triangleCount

def empty(a):
    pass

cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640, 240)
cv2.createTrackbar("threshold1", "TrackBars", 1, 500, empty)
cv2.createTrackbar("threshold2", "TrackBars", 31, 500, empty)

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
threshold1 = cv2.getTrackbarPos("threshold1", "TrackBars")
threshold2 = cv2.getTrackbarPos("threshold2", "TrackBars")

inputImg = cv2.imread("Resources/uas takimages/5.png")
imgHSV = cv2.cvtColor(inputImg, cv2.COLOR_BGR2HSV)

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
t_imgResult = cv2.bitwise_and(inputImg, inputImg, mask=trianglesMask)

imgResult = cv2.bitwise_or(GrassMaskResult, burntMaskResult)
imgResult = cv2.bitwise_or(imgResult, t_imgResult)

h_burnt = GetVerticesAmount(burntMaskResult)
h_grass = GetVerticesAmount(GrassMaskResult)
print(f'{np.array([[h_burnt, h_grass]])} (There are {h_burnt} house on the burnt grass and {h_grass} houses on the green grass)')


# cv2.imshow("original", img)
# cv2.imshow("HSV", imgHSV)
cv2.imshow("ImageResult", imgResult)
cv2.waitKey(0)

