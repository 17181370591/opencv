import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('1.jpg')

p=5

2D 卷积
操作如下：将核放在图像的一个像素 A 上，求与核对应的图像上 25（5x5）个像素的和，在取平均数，
用这个平均数替代像素 A 的值。重复以上操作直到将图像的每一个像素值都更新一边。
kernel = np.ones((p,p),np.float32)/p/p
dst1 = cv2.filter2D(img,-1,kernel)


这是由一个归一化卷积框完成的。他只是用卷积框覆盖区域所有像素的平均值来代替中心元素。
可以使用函数 cv2.blur() 和 cv2.boxFilter() 来完这个任务。
dst2=cv2.blur(img,(p,p))
dst3=cv2.boxFilter(img,-1,(p,p))


高斯模糊
dst4 = cv2.GaussianBlur(img,(5,5),0)


中值模糊
顾名思义就是用与卷积框对应像素的中值来替代中心像素的值。这个滤波器经常用来去除椒盐噪声。
前面的滤波器都是用计算得到的一个新值来取代中心像素的值，而中值滤波是用中心像素周围（也可以使他本身）的值来取代他。
他能有效的去除噪声。卷积核的大小也应该是一个奇数。
dst5 = cv2.medianBlur(img,5)


双边滤波
函数 cv2.bilateralFilter() 能在保持边界清晰的情况下有效的去除噪音，
这种方法会确保边界不会被模糊掉
dst6 = cv2.bilateralFilter(img,9,75,75)


def s(a,b):
    b='{}'.format(b)
    cv2.namedWindow(b,0)
    cv2.resizeWindow(b,500,500)
    cv2.imshow(b,a)
    cv2.waitKey(0)
  
s(img,'img')
s(dst1 ,'dst1')
s(dst2,'dst2')
s(dst3,'dst3')
s(dst4,'dst4')
s(dst5,'dst5')
s(dst6,'dst6')
