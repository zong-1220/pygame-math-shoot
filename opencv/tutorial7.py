import cv2

#img = cv2.imread('lenna.jpg')
img = cv2.imread('qq.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)#人臉辨識不用是彩色，先轉化為灰階
faceCascade = cv2.CascadeClassifier('face_detect.xml')#用CascadeClassifie函式載入檔案
faceRect = faceCascade.detectMultiScale(gray, 1.1, 5)#影片1:48:00左右;圖片,縮小倍率,縮小次數
print(len(faceRect))

for (x, y, w, h) in faceRect:
    cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), 2)


cv2.imshow('img', img)
cv2.waitKey(0)