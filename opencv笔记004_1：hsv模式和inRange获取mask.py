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




