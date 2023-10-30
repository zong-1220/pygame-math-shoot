#接續project5，把project5複製貼過來
#要解決三個顏色的筆，筆尖顏色不對的問題

from turtle import pencolor
import cv2
import numpy as np

cap = cv2.VideoCapture(0)


penColorHSV = [[85, 93, 158, 109, 244, 255],
                [57, 66, 84, 93, 140, 255],
                [120, 118, 154, 179, 255, 178]]

#新增另外兩個顏色，用列表來寫
penColorBGR= [[255, 0, 0],
                [0, 255, 0],
                [0, 0, 255]]

#用列表去記錄每一支筆滑過的位置及顏色
#每一個列表裡面會記錄XY座標跟顏色id[x, y, colorid],id如果是0則藍色,如果是1則綠色,如果是2則紅色
drawPoints = []

def findPen(img):

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    for i in range(len(penColorHSV)):
        lower = np.array(penColorHSV[i][:3])
        upper = np.array(penColorHSV[i][3:6])

        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(img, img, mask=mask)
        penx, peny = findContour(mask)
        cv2.circle(imgContour, (penx, peny), 10, penColorBGR[i], cv2.FILLED)
        #把penx跟peny記錄下來
        #如果peny不等於-1才記錄下來
        if peny!=-1:
            drawPoints.append([penx, peny, i])


def findContour(img):

    contours , hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h =-1, -1, -1, -1
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            peri = cv2.arcLength(cnt, True)
            vertices = cv2.approxPolyDP(cnt, peri * 0.02, True)
            x, y, w, h = cv2.boundingRect(vertices)

    return x+w//2,y

#新增一個函式
def draw(drawpoints):
    for point in drawpoints:
        #把它畫出來
        cv2.circle(imgContour, (point[0], point[1]), 10, penColorBGR[point[2]], cv2.FILLED)#複製貼上第35行，並加以修改，point裡面是2的原因為[x, y, colorid]，colorid是0,1,2第2個

while True:
    ret, frame = cap.read()
    if ret:
        imgContour = frame.copy()
        cv2.imshow('video', frame)
        findPen(frame)
        draw(drawPoints)#呼叫並且傳進來
        cv2.imshow('contour', imgContour)
    else:
        break
    
    if cv2.waitKey(1) ==ord('q'):#如果按下Q則影片結束
        break