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
