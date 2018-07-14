'''
有两类边界矩形。
　　直边界矩形 一个直矩形（就是没有旋转的矩形）。它不会考虑对象是否旋转。所以边界矩形的面积不是最小的。
  可以使用函数 cv2.boundingRect() 查找得到。
（x，y）为矩形左上角的坐标，（w，h）是矩形的宽和高。
x,y,w,h = cv2.boundingRect(cnt)
img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
 
旋转的边界矩形 这个边界矩形是面积最小的，因为它考虑了对象的旋转。用到的函数为 cv2.minAreaRect()。
返回的是一个 Box2D 结构，其中包含矩形中点的坐标（x，y），矩形的宽和高（w，h），以及旋转角度。
但是要绘制这个矩形需要矩形的 4 个角点，可以通过函数 cv2.boxPoints() 获得。
rect = cv2.minAreaRect(cnt)
box = cv2.boxPoints(rect)
box = np.int0(box)
im = cv2.drawContours(im,[box],0,(0,0,255),2)
'''




import numpy as np
import cv2

def f(contours):                #求轮廓列表里点最多的轮廓
    x=0
    p=0
    for i in range(len(contours)):
        if len(contours[i])>p:
            x=i
            p=len(contours[i])
    return x

def sh(img1,b='a'):                 #展示图片
    cv2.namedWindow(b,0)
    cv2.resizeWindow(b,500,500)
    cv2.imshow(b,img1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
yz=122
img1 = cv2.imread('4.jpg')
img = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
img=cv2.bitwise_not(img)
ret,thresh = cv2.threshold(img,yz,255,0)            

kernel = np.ones((15,15),np.uint8)
thresh=cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
thresh=cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)        #各种初始化


image,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,3)             #获取轮廓列表
xx=f(contours)
hull = cv2.convexHull(contours[xx])                             #求最大轮廓的凸包

img1 = cv2.imread('4.jpg')                                      #绘制凸包
img3= cv2.drawContours(img1, [hull], -1, (0,0,255),5)
sh(img3,'tu bao tu')

img1 = cv2.imread('4.jpg')                                          #绘制最大轮廓
img3= cv2.drawContours(img1, contours, xx, (0,0,255),5)
print(cv2.isContourConvex(contours[xx]))
sh(img3,'pu tong bian jie')

img1 = cv2.imread('4.jpg')                                      #绘制包围凸包的最小不旋转矩形
x,y,w,h = cv2.boundingRect(hull)               #contours[xx]    #获取边界矩形
cv2.rectangle(img1,(x,y),(x+w,y+h),(0,255,0),5)
print(x,y,w,h)
sh(img1,'ju xing bian jie')

img1 = cv2.imread('4.jpg')                                      #绘制包围凸包的最小旋转矩形
rect = cv2.minAreaRect(hull)        #contours[xx]     #获取选择边界矩形的中点，宽高，选择角度（逆时针为负数）
print('rect==',rect)
box = cv2.boxPoints(rect)                                       #获取矩形的四个顶点
print('box1==',box)
box = np.int0(box)                                               #小数取整
print('box2==',box)
im = cv2.drawContours(img1,[box],-1,(0,0,255),5)
sh(im,'xuan zhuan ju xing')
