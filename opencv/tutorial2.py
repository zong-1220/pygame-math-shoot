import cv2
import numpy as np
import random

img = cv2.imread('colorcolor.jpg')
#img = np.empty((300,300,3), np.uint8)#3是因為RGB，unit是代表0-255都是正整數，8是因為2的8次方0-255

# for row in range(300):
#     for col in range(300):
#         #img [row][col] = [255,0,0]#BGR
#         img [row][col] = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]#加上隨機
newImg = img[400:650, 100:500]#第一個值是高度，第二個值是高度

cv2.imshow('img', img)
cv2.imshow('newImg', newImg)
cv2.waitKey(0)