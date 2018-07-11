import cv2
import numpy as np
from matplotlib import pyplot as plt
'''
目标
　　• 本小节我们要学习直方图均衡化的概念，以及如何使用它来改善图片的对比。

原理
　　想象一下如果一副图像中的大多是像素点的像素值都集中在一个像素值范围之内会怎样呢？
  例如，如果一幅图片整体很亮，那所有的像素值应该都会很高。但是一副高质量的图像的像素值分布应该很广泛。
  所以你应该把它的直方图做一个横向拉伸（如下图），这就是直方图均衡化要做的事情。
  通常情况下这种操作会改善图像的对比度。
'''

#numpy的直方图均衡化
img = cv2.imread('4.jpg',0)
#flatten() 将数组变成一维
hist,bins = np.histogram(img.flatten(),256,[0,256])
# 计算累积分布图
cdf = hist.cumsum()
cdf_normalized = cdf * hist.max()/ cdf.max()
#plt.plot(cdf, color = 'g')
plt.plot(cdf_normalized, color = 'b')
plt.hist(img.flatten(),256,[0,256], color = 'r')
plt.xlim([0,256])
plt.legend(('cdf','histogram'), loc = 'upper left')
plt.show()

cdf_m = np.ma.masked_equal(cdf,0)
cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())
# 对被掩盖的元素赋值，这里赋值为 0   
cdf= np.ma.filled(cdf_m1,0).astype('uint8')           #这一段不能乱改变量，貌似是叠加操作

img = cdf[img]
cv2.imshow('',img)
cv2.imwrite('a.jpg',img)



#opencv的直方图均衡化
img = cv2.imread('1.jpg',0)
equ = cv2.equalizeHist(img)
#res = np.hstack((img,equ)) #stacking images side-by-side     
#cv2.imwrite('a.jpg',res)                    #注释掉的这两行是把新图和原图保存在一起进行对比
cv2.imshow('',equ)
cv2.imwrite('a.jpg',equ)

