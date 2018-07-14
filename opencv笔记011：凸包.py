'''
凸包
　　凸包与轮廓近似相似，但不同，虽然有些情况下它们给出的结果是一样的。
　　函数 cv2.convexHull() 可以用来检测一个曲线是否具有凸性缺陷，并能纠正缺陷。
  一般来说，凸性曲线总是凸出来的，至少是平的。如果有地方凹进去了就被叫做凸性缺陷。
  例如下图中的手。红色曲线显示了手的凸包，凸性缺陷被双箭头标出来了。
  效果相当于把几个突出的点连起来作为新的边界。
'''
'''
关于他的语法还有一些需要交代：
hull = cv2.convexHull(points[, hull[, clockwise[, returnPoints]]
参数：
　　• points 我们要传入的轮廓
　　• hull 输出，通常不需要
　　• clockwise 方向标志。如果设置为 True，输出的凸包是顺时针方向的。否则为逆时针方向。
　　• returnPoints 默认值为 True。它会返回凸包上点的坐标。如果设置为 False，就会返回与凸包点对应的轮廓上的点。
要获得上图的凸包，下面的命令就够了：
hull = cv2.convexHull(cnt)
但是如果你想获得凸性缺陷，需要把 returnPoints 设置为 False。以上面的矩形为例，首先我们找到他的轮廓 cnt。
现在我把 returnPoints 设置为 True 查找凸包，我得到下列值：
[[[234 202]], [[ 51 202]], [[ 51 79]], [[234 79]]]，其实就是矩形的四个角点。
现在把 returnPoints 设置为 False，我得到的结果是[[129],[ 67],[ 0],[142]]。他们是轮廓点的索引。
例如：cnt[129] = [[234,202]]，这与前面我们得到结果的第一个值是一样的。
在凸检验中你我们还会遇到这些。
'''


import numpy as np
import cv2


yz=88
img1 = cv2.imread('4.jpg')
img = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
img=cv2.bitwise_not(img)
ret,thresh = cv2.threshold(img,yz,255,0)            #灰度图，取反，二值化


kernel = np.ones((15,15),np.uint8)
thresh=cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)         #去掉噪声
thresh=cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)        #填满内部 


image,contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,3)
hull = cv2.convexHull(contours[0])                      #第一个参数是轮廓


img3= cv2.drawContours(img1, [hull], -1, (0,0,255),2)
#img3= cv2.drawContours(img1, contours, -1, (0,0,255),2)
cv2.namedWindow('a',0)
cv2.resizeWindow('a',500,500)
cv2.imshow('a',img3)
#凸性检测:函数 cv2.isContourConvex() 可以可以用来检测一个曲线是不是凸的。它只能返回 True 或 False。
b= cv2.convexHull(contours[0],returnPoints=False)           #返回的是凸包上的点在轮廓上的索引
print(np.where(contours[0][b.flatten()]!=hull))             #可以发现确实是索引，这里返回空值

k = cv2.isContourConvex(cnt)
