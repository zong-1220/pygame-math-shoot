import cv2
#以下是讀取圖片
img = cv2.imread('colorcolor.jpg')

#img = cv2.resize(img, (300,300))#改變圖片尺寸為300*300象素
img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)#圖片改為原本的0.5倍
cv2.imshow('img', img)  #用imshow這個函式
cv2.waitKey(10) #一千毫秒=一秒鐘，如果輸入0就是無限久的時間，按下任一鍵則回傳數值導致畫面關閉

#以下是讀取影片
#cap = cv2.VideoCapture('thumb.mp4')
cap = cv2.VideoCapture(0)#如果這樣寫，則會開啟視訊鏡頭，數字寫1則是外接鏡頭

while True:
    ret, frame = cap.read()#這個函式會回傳兩個值，一個是有沒有成功用ret變數代表true or false，另一個是下一張圖片用frame表示
    if ret:#有取得成功的話
        frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
        cv2.imshow('video', frame)
    else:
        break
    #cv2.waitKey(1)#如數字增加則影片速度變慢
    if cv2.waitKey(10) ==ord('q'):#如果按下Q則影片結束
        break