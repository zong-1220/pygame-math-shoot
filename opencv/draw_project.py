import cv2
import numpy as np
#複製tutorial1的程式，取得攝影機畫面

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()#這個函式會回傳兩個值，一個是有沒有成功用ret變數代表true or false，另一個是下一張圖片用frame表示
    if ret:#有取得成功的話
        cv2.imshow('video', frame)
    else:
        break
    #cv2.waitKey(1)#如數字增加則影片速度變慢
    if cv2.waitKey(1) ==ord('q'):#如果按下Q則影片結束
        break