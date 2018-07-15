import cv2,time
import numpy as np
from matplotlib import pyplot as plt

def f(contours):                                                #求轮廓列表里点最多的轮廓
    x=0
    p=0
    for i in range(len(contours)):
        if len(contours[i])>p:
            x=i
            p=len(contours[i])
    return x
pic='4.jpg'
img2= cv2.imread(pic)
img1 = cv2.imread(pic,0)
a,img1=cv2.threshold(img1,111,255,0)
x,cnt,x=cv2.findContours(img1,cv2.RETR_TREE,3)
x=f(cnt)
img3=np.zeros_like(img1)
z=cv2.drawContours(img3,cnt,x,255,-1)
a=(z.shape[1],z.shape[0])
b=(np.int(z.shape[1]/2),np.int(z.shape[0]/2))
i=30
while 1:
    M=cv2.getRotationMatrix2D(b,i,1)
    p=cv2.warpAffine(z,M,a)
    #p=np.zeros_like(img1)
    plt.subplot(1,2,1)
    plt.imshow(z)
    plt.subplot(1,2,2)
    plt.imshow(p)   
    x=cv2.matchShapes(z,p,1,0)
    print(x)
    plt.ion()
    plt.pause(1.3)
    plt.close()
    i+=30

