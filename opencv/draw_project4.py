#先複製draw_project3程式
#接著要偵測筆的輪廓，再去偵測筆的筆尖
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

def findPen(img):
    #複製貼上draw_project2的36-42行程式
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower = np.array([85, 93, 158])#修改視訊畫面偵測藍色的最小值
    upper = np.array([109, 244, 255])#修改視訊畫面偵測藍色的最大值

    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)
    #findContour(mask)#新增這一行，把mask遮罩傳進來
    penx, peny = findContour(mask)#新增這一行
    cv2.circle(imgContour, (penx, peny), 10, (255,0,0), cv2.FILLED)#新增這一行，把這個點給畫圓出來;畫在imgContour這張圖上面,圓中心點,半徑10，藍色，填滿
    cv2.imshow('result', result)

def findContour(img):
    ##複製tutorial6的8-23行，並且刪除一些不用的程式
    contours , hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)#canny改成img
    x, y, w, h =-1, -1, -1, -1#新增這一行,因為有可能全部面積不大於500，所以先設定好
    for cnt in contours:
        cv2.drawContours(imgContour, cnt, -1, (255,0,0), 4)
        area = cv2.contourArea(cnt)
        if area > 500:
            peri = cv2.arcLength(cnt, True)
            vertices = cv2.approxPolyDP(cnt, peri * 0.02, True)
            x, y, w, h = cv2.boundingRect(vertices)#筆尖是用boundingRect這個值來設定

    return x+w//2,y#新增這一行,把筆尖的點回傳出去

while True:
    ret, frame = cap.read()
    if ret:
        imgContour = frame.copy()#新增這一行
        cv2.imshow('video', frame)
        findPen(frame)
        cv2.imshow('contour', imgContour)#新增這一行
    else:
        break
    
    if cv2.waitKey(1) ==ord('q'):#如果按下Q則影片結束
        break