'''
image为输入图像，需要灰度图

method为检测方法,常用CV_HOUGH_GRADIENT

dp为检测内侧圆心的累加器图像的分辨率于输入图像之比的倒数，如dp=1，累加器和输入图像具有相同的分辨率，如果dp=2，累计器便有输入图像一半那么大的宽度和高度

minDist表示两个圆之间圆心的最小距离

param1有默认值100，它是method设置的检测方法的对应的参数，对当前唯一的方法霍夫梯度法cv2.HOUGH_GRADIENT，它表示传递给canny边缘检测算子的高阈值，而低阈值为高阈值的一半

param2有默认值100，它是method设置的检测方法的对应的参数，对当前唯一的方法霍夫梯度法cv2.HOUGH_GRADIENT，它表示在检测阶段圆心的累加器阈值，它越小，就越可以检测到更多根本不存在的圆，而它越大的话，能通过检测的圆就更加接近完美的圆形了

minRadius有默认值0，圆半径的最小值

maxRadius有默认值0，圆半径的最大值
'''

import cv2
import numpy as np
img = cv2.imread('o.jpg',0)
img = cv2.medianBlur(img,5)
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
dp=1
minDist=20
param1=100
#e=cv2.Canny(img,param1/2,param1)

circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,dp,minDist,
param1=param1,param2=70,minRadius=80,maxRadius=0)
circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
cv2.imshow('detected circles',cimg)


