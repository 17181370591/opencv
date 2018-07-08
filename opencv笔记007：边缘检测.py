#Canny 边缘检测
#http://www.cnblogs.com/Undo-self-blog/p/8436480.html
#通过调节滑动条来设置阈值 minVal 和 maxVal 进而来进行 Canny 边界检测。这样你就会理解阈值的重要性了。


import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('2.jpg',0)
a,b=100,200
cv2.namedWindow('a')
def nothing(x):
    pass

cv2.createTrackbar('low','a',100,200,nothing)
cv2.createTrackbar('high','a',0,255,nothing)


while 1:
    a=cv2.getTrackbarPos('low','a')
    b=cv2.getTrackbarPos('high','a')
    print(a,b)
    edges = cv2.Canny(img,a,b)
    cv2.imshow('a',edges)
    cv2.waitKey(1000)
