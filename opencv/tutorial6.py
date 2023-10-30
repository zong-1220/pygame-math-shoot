from pickle import TRUE
import cv2

img = cv2.imread('shape.jpg')
imgContour = img.copy()
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)#檢測輪廓不需要彩色
canny = cv2.Canny(img, 150, 200)#檢測邊緣
contours , hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)#之後再去檢測輪廓;第一個參數式偵測的圖片,第二個是檢測模式(外輪廓),第三個參數是寫不做任何壓縮
#這個函式會回傳兩個參數值，第一個是回傳的輪廓的值用變數contours表示，第二個是回傳一個階層用hierarchy表示 

for cnt in contours:
    #print(cnt)#印出所有輪廓點
    cv2.drawContours(imgContour, cnt, -1, (255,0,0), 4)#畫出來;畫哪張圖,畫的輪廓,畫第幾個(每一個都話就是-1),顏色,粗度
    #print(cv2.contourArea(cnt))#取得輪廓面積並印出來
    area = cv2.contourArea(cnt)
    if area > 500:#用面積過濾為0的雜訊
        #print(cv2.arcLength(cnt, True))#取得輪廓總長;是閉合的寫True
        peri = cv2.arcLength(cnt, True)
        vertices = cv2.approxPolyDP(cnt, peri * 0.02, True)#多邊形有幾個頂點
        #print(len(vertices))#幾個邊印出來(因為沒有八邉型，所以出現8是圓形)
        corners = len(vertices)
        x, y, w, h = cv2.boundingRect(vertices)#把每一個圖形用一個框形框起來;xy座標是左上角的座標
        cv2.rectangle(imgContour, (x,y), (x+w, y+h), (0,255,0), 4)#把方形畫出來;畫哪張圖,左上角座標,右上角座標跟高度,顏色,粗度
        if corners == 3:
            cv2.putText(imgContour, 'triangle', (x,y-5), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
        elif corners == 4:
            cv2.putText(imgContour, 'rectangle', (x,y-5), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
        elif corners == 5:
            cv2.putText(imgContour, 'pentagon', (x,y-5), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
        elif corners >= 6:
            cv2.putText(imgContour, 'circle', (x,y-5), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
            
cv2.imshow('img', img)
cv2.imshow('canny', canny)
cv2.imshow('imgContour', imgContour)
cv2.waitKey(0)