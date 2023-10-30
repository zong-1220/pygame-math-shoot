#先複製draw_project4程式，draw_project4會把藍色筆尖顯示完成
#這個程式是接著顯示其他顏色
#完成時將可以顯示出三個顏色的筆尖
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

#去draw_project2執行該程式，找出綠色跟紅色最小跟最大值
#blue green red
#新增下面三行
penColorHSV = [[85, 93, 158, 109, 244, 255],#前三個值最小值，後三個值最大值
                [57, 66, 84, 93, 140, 255],
                [120, 118, 154, 179, 255, 178]]

def findPen(img):

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    for i in range(len(penColorHSV)):#新增FOR迴圈,讓他去偵測每一個顏色
        #lower = np.array([85, 93, 158])#藍色最小
        lower = np.array(penColorHSV[i][:3])#前三個
        #upper = np.array([109, 244, 255])#藍色最大
        upper = np.array(penColorHSV[i][3:6])#後三個

        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(img, img, mask=mask)
        penx, peny = findContour(mask)
        cv2.circle(imgContour, (penx, peny), 10, (255,0,0), cv2.FILLED)
    #cv2.imshow('result', result)#新增註解掉這一行

def findContour(img):

    contours , hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h =-1, -1, -1, -1
    for cnt in contours:
        #cv2.drawContours(imgContour, cnt, -1, (255,0,0), 4)把顯示輪廓註解掉讓效果好一點
        area = cv2.contourArea(cnt)
        if area > 500:
            peri = cv2.arcLength(cnt, True)
            vertices = cv2.approxPolyDP(cnt, peri * 0.02, True)
            x, y, w, h = cv2.boundingRect(vertices)

    return x+w//2,y

while True:
    ret, frame = cap.read()
    if ret:
        imgContour = frame.copy()
        cv2.imshow('video', frame)
        findPen(frame)
        cv2.imshow('contour', imgContour)
    else:
        break
    
    if cv2.waitKey(1) ==ord('q'):#如果按下Q則影片結束
        break