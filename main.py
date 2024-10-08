import cv2
import numpy as np

#Function to get number of triangle
def get_num_triangle(img):
    imgBlur = cv2.GaussianBlur(img, (7, 7), 1)
    imgCanny = cv2.Canny(imgBlur, 500, 500)
    contours, _ = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    triangleCount = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            objNum = len(approx)
            if objNum == 3:
                triangleCount += 1
    return triangleCount

#importing img
inputImg = cv2.imread("Resources/uas takimages/5.png")
imgHSV = cv2.cvtColor(inputImg, cv2.COLOR_BGR2HSV)

#Creating grass mask
grassMask = cv2.inRange(imgHSV, np.array([36, 108, 0]), np.array([117, 255, 255]))
g_mask_bgr = cv2.cvtColor(grassMask, cv2.COLOR_GRAY2BGR)
cyanMask = np.zeros_like(g_mask_bgr)
cyanMask[:] = [251, 252, 102]
GrassMaskResult = cv2.bitwise_and(cyanMask, g_mask_bgr, mask=grassMask)

#Creating burnt mask
burntMask = cv2.inRange(imgHSV, np.array([1, 108, 0]), np.array([36, 255, 255]))
mask_bgr = cv2.cvtColor(burntMask, cv2.COLOR_GRAY2BGR)
yellowMask = np.zeros_like(mask_bgr)
yellowMask[:] = [102, 252, 252]
burntMaskResult = cv2.bitwise_and(yellowMask, mask_bgr, mask=burntMask)

#Creating triangle Mask
i_trianglesMask = cv2.inRange(imgHSV, np.array([1, 108, 0]), np.array([117, 255, 255]))
trianglesMask = cv2.bitwise_not(i_trianglesMask)
t_imgResult = cv2.bitwise_and(inputImg, inputImg, mask=trianglesMask)

#Resultant image
imgResult = cv2.bitwise_or(GrassMaskResult, burntMaskResult)
imgResult = cv2.bitwise_or(imgResult, t_imgResult)

#Calculating number of house in each region
h_burnt = get_num_triangle(burntMaskResult)
h_grass = get_num_triangle(GrassMaskResult)
print(f'{np.array([[h_burnt, h_grass]])} (There are {h_burnt} house on the burnt grass and {h_grass} houses on the green grass)')

cv2.imshow("ImageResult", imgResult)
cv2.waitKey(0)

