#複製draw_project程式
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

def findPen(img):
    #複製貼上draw_project2的36-42行程式
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)#新增這一行，剪下貼上第26行，把每一幀的圖片轉換成hsv

    lower = np.array([85, 93, 158])#修改視訊畫面偵測藍色的最小值
    upper = np.array([109, 244, 255])#修改視訊畫面偵測藍色的最大值

    mask = cv2.inRange(hsv, lower, upper)#過濾顏色;過濾的圖片,色調飽和度亮度最小值,色調飽和度亮度最大值
    result = cv2.bitwise_and(img, img, mask=mask)

    cv2.imshow('result', result)#新增這一行

while True:
    ret, frame = cap.read()#這個函式會回傳兩個值，一個是有沒有成功用ret變數代表true or false，另一個是下一張圖片用frame表示
    if ret:#有取得成功的話
        cv2.imshow('video', frame)
        findPen(frame)#新增這一行，把每一幀傳進去
    else:
        break
    #cv2.waitKey(1)#如數字增加則影片速度變慢
    if cv2.waitKey(1) ==ord('q'):#如果按下Q則影片結束
        break