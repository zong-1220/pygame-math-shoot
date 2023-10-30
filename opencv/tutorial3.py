import cv2
import numpy as np

kernel = np.ones((3,3), np.uint8)#數字越大越膨脹
kernel2 = np.ones((3,3), np.uint8)

img = cv2.imread('colorcolor.jpg')
img = cv2.resize(img,(0,0),fx=0.5,fy=0.5)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)#彩色轉換成黑白
blur = cv2.GaussianBlur(img, (5,5), 2)#高斯模糊，中間的數字只能填奇數13579，中間是合最後面是標準差
canny = cv2.Canny(img, 150, 200)#邊緣圖片，中間數值是邊緣相差最小值，右邊是邊緣相差最大值
dilate = cv2.dilate(canny, kernel, iterations=1)#膨脹效果，iterations=1是膨脹1次
erode = cv2.erode(dilate,kernel2, iterations=1)#線條變細

cv2.imshow('img', img)#前面是視窗名稱
cv2.imshow('gray', gray)
cv2.imshow('blur', blur)
cv2.imshow('canny', canny)
cv2.imshow('dilate', dilate)
cv2.imshow('erode', erode)
cv2.waitKey(0)
