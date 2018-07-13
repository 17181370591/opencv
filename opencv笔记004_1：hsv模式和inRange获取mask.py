import numpy as np
import cv2,time
from matplotlib import pyplot as plt


im1=cv2.imread('p.jpg')


hsv=cv2.cvtColor(im1,cv2.COLOR_BGR2HSV)                   #将pic转成hsv格式，和原图颜色不一样
lb,hb=np.array([0,180,110]),np.array([55,255,255])
mask=cv2.inRange(hsv,lb,hb)
res=cv2.bitwise_and(im1,im1,mask=mask)                    #黄色部分显示原图，其他部分全黑色
#res=cv2.bitwise_and(hsv,hsv,mask=mask)
cv2.imshow('',res)
cv2.waitKey()
cv2.destroyAllWindows()


f1,f2=np.array([66,66,130]),np.array([111,100,150])
f3,f4=np.array([16,120,140]),np.array([121,190,210])
f5,f6=np.array([46,100,40]),np.array([122,180,80])
mask1=cv2.inRange(im1,f1,f2)                              #rgb图像用inRange
mask3=cv2.inRange(im1,f3,f4)
mask5=cv2.inRange(im1,f5,f6)

mask=cv2.add(cv2.add(mask1,mask3),mask5)

mi=cv2.bitwise_not(mask)
ma=cv2.bitwise_and(im1,im1,mask=mask)

ma1=cv2.cvtColor(im1,cv2.COLOR_BGR2GRAY)
ma1=cv2.bitwise_and(ma1,ma1,mask=mi)
ma1=np.repeat(ma1.flatten(),3).reshape(im1.shape)

ma=cv2.add(ma1,ma)                                          #mask部分显示原图，其他部分显示对应灰度图
cv2.imshow('',ma)
k=cv2.waitKey(5)&0xFF

'''
#x需要三层括号，相当于一个像素点。因为img的shape是a*b*3的
min1=min(r,g,b)
max1=max(r,g,b)
x=np.uint8([[[0,0,255]]])
y=cv2.cvtColor(x,cv2.COLOR_BGR2HSV)
蓝色255,0,0对应120,255,255
绿色0，255,0对应60,255,255
红色0,0，255对应0,255,255
黄色0，255,255对应30,255,255
紫色255,0，255对应150,255,255
青色255,255,0对应90,255,255
hsv的s表示饱和度，min1越大饱和度越低，算法应该是(max1-min1)/max1*255，v表示明度，max1越打明度越大
'''


============================================================================

#用滚动条实时展示inRange效果
#滚动条获取当前rgb值，加减de获取上限和下限，用位加法运算获取图片

import numpy as np
import cv2,time
from matplotlib import pyplot as plt

def nn(x):pass
im1=cv2.imread('p.jpg')

de=60                                                           
cv2.namedWindow('a',0)
cv2.resizeWindow('a',800,600)
cv2.createTrackbar('r','a',0,255,nn)
cv2.createTrackbar('g','a',0,255,nn)
cv2.createTrackbar('b','a',0,255,nn)
while 1:
    r=cv2.getTrackbarPos('r','a')
    g=cv2.getTrackbarPos('g','a')
    b=cv2.getTrackbarPos('b','a')
    m=np.uint8([r,g,b])
    #print(m)
    m1,m2=m-de,m+de
    mask=cv2.inRange(im1,m1,m2)
    im=cv2.bitwise_and(im1,im1,mask=mask)
    cv2.imshow('a',im)
    cv2.waitKey(111)

