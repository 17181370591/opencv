# -*- coding: utf-8 -*-


"""
图像梯度
目标
• 图像梯度，图像边界等
• 使用到的函数有：cv2.Sobel()，cv2.Schar()，cv2.Laplacian() 等
原理
梯度简单来说就是求导。
OpenCV 提供了三种不同的梯度滤波器，或者说高通滤波器：Sobel，Scharr 和 Laplacian。我们会意义介绍他们。
Sobel，Scharr 其实就是求一阶或二阶导数。Scharr 是对 Sobel（使用小的卷积核求解求解梯度角度时）的优化。
Laplacian 是求二阶导数。

18.1 Sobel  算子和 Scharr  算子
Sobel 算子是高斯平滑与微分操作的结合体，所以它的抗噪声能力很好。
你可以设定求导的方向（xorder 或 yorder）。还可以设定使用的卷积核的大小（ksize）。
如果 ksize=-1，会使用 3x3 的 Scharr 滤波器，它的的效果要比 3x3 的 Sobel 滤波器好（而且速度相同，
所以在使用 3x3 滤波器时应该尽量使用 Scharr 滤波器）。3x3 的 Scharr 滤波器卷积核如下：
x 方向
-3 0 3
-10 0 10
-3 0 3
y 方向
-3 -10 -3
0 0 0
3 10 3
"""


import cv2
import numpy as np
from matplotlib import pyplot as plt
img=cv2.imread('a1.jpg',0)
#cv2.CV_64F 输出图像的深度（数据类型），可以使用 -1, 与原图像保持一致 np.uint8
laplacian=cv2.Laplacian(img,cv2.CV_64F)
# 参数 1,0 为只在 x 方向求一阶导数，最大可以求 2 阶导数。
sobelx=cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
# 参数 0,1 为只在 y 方向求一阶导数，最大可以求 2 阶导数。
sobely=cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)

sox=cv2.Sobel(img,cv2.CV_64F,1,0,ksize=-1)
soy=cv2.Sobel(img,cv2.CV_64F,0,1,ksize=-1)

plt.subplot(2,3,1),plt.imshow(img,cmap = 'gray')
plt.title('Original'), plt.xticks([]), plt.yticks([])
plt.subplot(2,3,2),plt.imshow(laplacian,cmap = 'gray')
plt.title('Laplacian'), plt.xticks([]), plt.yticks([])
plt.subplot(2,3,3),plt.imshow(sobelx,cmap = 'gray')
plt.title('Sobel X'), plt.xticks([]), plt.yticks([])
plt.subplot(2,3,4),plt.imshow(sobely,cmap = 'gray')
plt.title('Sobel Y'), plt.xticks([]), plt.yticks([])
plt.subplot(2,3,5),plt.imshow(sox,cmap = 'gray')
plt.title('Sxxxxx-1'), plt.xticks([]), plt.yticks([])
plt.subplot(2,3,6),plt.imshow(soy,cmap = 'gray')
plt.title('yyyyy-1'), plt.xticks([]), plt.yticks([])
plt.show()
