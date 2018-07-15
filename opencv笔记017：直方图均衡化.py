#http://www.cnblogs.com/Undo-self-blog/p/8439149.html
#不知道有什么用。。

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
'''
OpenCV 中的直方图均衡化函数为 cv2.equalizeHist()。
这个函数的输入图片仅仅是一副灰度图像，输出结果是直方图均衡化之后的图像。
下边的代码还是对上边的那幅图像进行直方图均衡化：
'''
img = cv2.imread('1.jpg',0)
equ = cv2.equalizeHist(img)
#res = np.hstack((img,equ)) #stacking images side-by-side     
#cv2.imwrite('a.jpg',res)                    #注释掉的这两行是把新图和原图保存在一起进行对比
cv2.imshow('',equ)
cv2.imwrite('a.jpg',equ)



'''
CLAHE

　　有限对比适应性直方图均衡化我们在上边做的直方图均衡化会改变整个图像的对比度，
  但是在很多情况下，这样做的效果并不好。例如，下图分别是输入图像和进行直方图均衡化之后的输出图像。

　　的确在进行完直方图均衡化之后，图片背景的对比度被改变了。但是你再对比一下两幅图像中雕像的面图，
  由于太亮我们丢失了很多信息。造成这种结果的根本原因在于这幅图像的直方图并不是集中在某一个区域（试着画出它的直方图，
  你就明白了）。为了解决这个问题，我们需要使用自适应的直方图均衡化。
  这种情况下，整幅图像会被分成很多小块，这些小块被称为“tiles”（在 OpenCV 中 tiles 的大小默认是 8x8），
  然后再对每一个小块分别进行直方图均衡化（跟前面类似）。
　　所以在每一个的区域中，直方图会集中在某一个小的区域中（除非有噪声干扰）。如果有噪声的话，噪声会被放大。
  为了避免这种情况的出现要使用对比度限制。对于每个小块来说，如果直方图中的 bin 超过对比度的上限的话，
  就把其中的像素点均匀分散到其他 bins 中，然后在进行直方图均衡化。
  最后，为了去除每一个小块之间“人造的”（由于算法造成）边界，再使用双线性差值，对小块进行缝合。
下面的代码显示了如何使用 OpenCV 中的 CLAHE。
'''

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
cl1 = clahe.apply(img)
cv2.imwrite('a2.jpg',cl1)

'''
#rgb图像split成单通道后，也可以用这个来改变每个通道的对比度，然后merge成rgb图像（自己想到的，似乎效果还可以）
img = cv2.imread('1.jpg')
r,g,b=cv2.split(img)

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
r2 = clahe.apply(r)
g2 = clahe.apply(g)
b2 = clahe.apply(b)
img2=cv2.merge((r2,g2,b2))
'''



'''
2D 直方图

目标
　　本节我们会学习如何绘制 2D 直方图，我们会在下一节中使用到它。
22.3.1 介绍
　　在前面的部分我们介绍了如何绘制一维直方图，之所以称为一维，是因为我们只考虑了图像的一个特征：灰度值。
  但是在 2D 直方图中我们就要考虑两个图像特征。对于彩色图像的直方图通常情况下我们需要考虑每个的颜色（Hue）和
  饱和度（Saturation）。根据这两个特征绘制 2D 直方图。
OpenCV 的官方文档中包含一个创建彩色直方图的例子。本节就是要和大家一起来学习如何绘制颜色直方图，
这会对我们下一节学习直方图投影有所帮助。


22.3.2 OpenCV 中的 2D 直方图
　　使用函数 cv2.calcHist() 来计算直方图既简单又方便。如果要绘制颜色直方图的话，
  我们首先需要将图像的颜色空间从 BGR 转换到 HSV。（记住，计算一维直方图，要从 BGR 转换到 HSV）。
  计算 2D 直方图，函数的参数要做如下修改：
　　• channels=[0 ，1] 因为我们需要同时处理 H 和 S 两个通道。
　　• bins=[180 ，256]H 通道为 180，S 通道为 256。
　　• range=[0 ，180 ，0 ，256]H 的取值范围在 0 到 180，S 的取值范围在 0 到 256。
代码如下：
'''
img = cv2.imread('3.jpg')
hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

hist =cv2.calcHist([hsv], [0, 1], None, [180, 256],[0, 180, 0, 256])
plt.imshow(hist,interpolation = 'nearest')
plt.show()
