import cv2
import numpy as np

img = np.zeros((600,600,3), np.uint8)#zeros這個函式是裡面都是0，所以會是黑色
#cv2.line(img, (0,0), (400,300), (255,0,0), 1)#圖片,起始點,終點,顏色BGR,粗度
cv2.line(img, (0,0), (img.shape[1],img.shape[0]), (255,0,0), 1)#img.shape[1]寬度,img.shape[0]高度
#cv2.rectangle(img, (0,0),(400,300),(0,0,255), 1)#起始左上，終點右下
cv2.rectangle(img, (0,0),(400,300),(0,0,255), cv2.FILLED)#填滿cv2.FILLED
cv2.circle(img, (300,400), 30, (255,0,0), 3)#圖片,圓心,半徑,顏色,粗度 
cv2.putText(img,'hello', (100,500), cv2.FONT_HERSHEY_COMPLEX,3, (255,255,255), 2)#圖,文字內容,文字左下角的座標,字體,文字大小,顏色,粗度;putText函式不支援中文



cv2.imshow('img', img)
cv2.waitKey(0)