'''
形状匹配
函数 cv2.matchShape() 可以帮我们比较两个形状或轮廓的相似度。如果返回值越小，匹配越好。
它是根据 Hu  矩来计算的。似乎图片的尺寸和旋转对匹配值几乎没有影响。
下面的代码使用了随机尺寸+循环旋转进行测试
'''

import cv2,time,random
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
    ran=random.random()*2
    M=cv2.getRotationMatrix2D(b,i,ran)
    p=cv2.warpAffine(z,M,a)
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
    if i>333:
        break

