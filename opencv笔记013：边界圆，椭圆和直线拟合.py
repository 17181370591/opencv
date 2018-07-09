'''
最小外接圆
　　函数 cv2.minEnclosingCircle() 可以帮我们找到一个对象的外切圆。
　　它是所有能够包括对象的圆中面积最小的一个。
  
椭圆拟合
　　使用的函数为 cv2.ellipse()，返回值其实就是旋转边界矩形的内切圆。
  
直线拟合
　　我们可以根据一组点拟合出一条直线，同样我们也可以为图像中的白色点拟合出一条直线。 
'''


import numpy as np
import cv2

def f(contours):                            #求轮廓列表里点最多的轮廓
    x=0
    p=0
    for i in range(len(contours)):
        if len(contours[i])>p:
            x=i
            p=len(contours[i])
    return x

def sh(img1,b='a'):                         #展示图片
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
thresh=cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)             #各种初始化


image,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,3)          #获取轮廓列表
xx=f(contours)
hull = cv2.convexHull(contours[xx])                                 #绘制凸包

img1 = cv2.imread('4.jpg')
img3= cv2.drawContours(img1, [hull], -1, (0,0,255),5)
sh(img3,'tu bao tu')



img1 = cv2.imread('4.jpg')                                            #最小外接圆
(x,y),radius = cv2.minEnclosingCircle(contours[xx])                 #返回圆心坐标和半径
center = (int(x),int(y))
radius = int(radius)
img = cv2.circle(img1,center,radius,(0,255,0),5)
sh(img,'yuan')



img1 = cv2.imread('4.jpg')                                      #旋转边界矩形的内切椭圆
#下面的ellipse1返回中点坐标，两个直径？，选择角度，但数值和旋转边界矩不一样，似乎是因为宽高和两个直径的顺序是相反的
ellipse1 = cv2.fitEllipse(contours[xx])                        
img = cv2.ellipse(img1,ellipse1,(0,255,0),5)
sh(img,'tuo yuan')



img1 = cv2.imread('4.jpg')
rows,cols = img1.shape[:2]
[vx,vy,x,y] = cv2.fitLine(contours[xx],cv2.DIST_L2,0,0.01,0.01)
#y=kx+b所以b=-x*k+y，注意坐标轴在y轴上是反的
lefty = int((-x*vy/vx) + y)
'''
教程的写法是
righty = int(((cols-x)*vy/vx)+y)
img = cv2.line(img,(cols-1,righty),(0,lefty),(0,255,0),2)
教程的思路是如果直线经过(a,b)和(c,d)，那么d=(c-a)*k+b，这样通过中点求出了上边界与直线的交点，
但画图时使用了(cols-1,righty)而不是(cols,righty)，不知道是不是笔误。
下面两行是我自己写的，upx是直线与x轴的交点的x坐标
'''
upx=-lefty*vx/vy
img = cv2.line(img1,(upx,0),(0,lefty),(0,255,0),2)


sh(img,'zhi xian')
