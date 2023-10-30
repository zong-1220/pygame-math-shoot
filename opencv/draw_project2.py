#複製tutorial5的程式，並且加上修改

import cv2
import numpy as np

def empty(v):
    pass

#img = cv2.imread('xiWinnie.jpg')
#img = cv2.resize(img,(0,0),fx=0.5,fy=0.5)
cap = cv2.VideoCapture(0)#增加這一行，並且將上面註解掉

#創建視窗
cv2.namedWindow('TrackBar')
cv2.resizeWindow('TrackBar', 640, 320)

#創建控制條
cv2.createTrackbar('Hue Min', 'TrackBar', 0, 179, empty)#色調
cv2.createTrackbar('Hue Max', 'TrackBar', 179, 179, empty)
cv2.createTrackbar('Sat Min', 'TrackBar', 0, 255, empty)#飽和度
cv2.createTrackbar('Sat Max', 'TrackBar', 255, 255, empty)
cv2.createTrackbar('Val Min', 'TrackBar', 0, 255, empty)#亮度
cv2.createTrackbar('Val Max', 'TrackBar', 255, 255, empty)


while True:
    h_min = cv2.getTrackbarPos('Hue Min', 'TrackBar')#控制條的名稱、視窗的名稱
    h_max = cv2.getTrackbarPos('Hue Max', 'TrackBar')
    s_min = cv2.getTrackbarPos('Sat Min', 'TrackBar')
    s_max = cv2.getTrackbarPos('Sat Max', 'TrackBar')
    v_min = cv2.getTrackbarPos('Val Min', 'TrackBar')
    v_max = cv2.getTrackbarPos('Val Max', 'TrackBar')
    print(h_min, h_max, s_min, s_max, v_min, v_max)

    ret, img = cap.read()#新增這一行，讀取每一幀的畫面，回傳兩個值，讀取有沒有成功ret,每一幀的圖片img
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)#新增這一行，剪下貼上第26行，把每一幀的圖片轉換成hsv

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    mask = cv2.inRange(hsv, lower, upper)#過濾顏色;過濾的圖片,色調飽和度亮度最小值,色調飽和度亮度最大值
    result = cv2.bitwise_and(img, img, mask=mask)

    cv2.imshow('img', img)
    #cv2.imshow('hsv', hsv)新增這一行，把它註解掉不讓它顯示
    cv2.imshow('mask', mask)
    cv2.imshow('result', result)
    cv2.waitKey(1)

