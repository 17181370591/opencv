#仿射变换类似于css的倾斜skew，一个矩形变换完后是个平行四边形
#透视常用于将四边形转换成矩形，类似于将照片拉伸裁剪成证件照的操作
#仿射变换后平行四边形的各边仍操持平行，透视变换结果允许是梯形等四边形，所以仿射变换是透视变换的子集

import numpy as np
import cv2,time
from matplotlib import pyplot as plt

def nn(x):
  pass
im1=cv2.imread('2.jpg')



#resize改变尺寸，一种是传入变换后的尺寸，一种是传入变换后的比值
im2=cv2.resize(im1,(500,500))
im3=cv2.resize(im1,None,fx=.5,fy=.6)




'''
图像的平移

下面介绍的图像操作假设你已经知道了为什么需要用矩阵构造才能实现了（上面那个博客有介绍为什么）。
那么关于偏移很简单，图像的平移，沿着x方向tx距离，y方向ty距离，那么需要构造移动矩阵： 
M=[1001txty]
M=[10tx01ty]

通过numpy来产生这个矩阵，并将其赋值给仿射函数cv2.warpAffine(). 
仿射函数cv2.warpAffine()接受三个参数，需要变换的原始图像，
移动矩阵M 以及变换的图像大小（这个大小如果不和原始图像大小相同，那么函数会自 动通过插值来调整像素间的关系）。
'''

H = np.float32([[1,0,100],[0,1,50]])                          #平移矩阵
rows,cols = im1.shape[:2]
res = cv2.warpAffine(im1,H,(cols,rows))                       #需要图像、变换矩阵、变换后的大小
plt.subplot(121)
plt.imshow(im1)
plt.subplot(122)
plt.imshow(res)
#plt.show()




#图像的旋转+平移+缩放
#下面的变形是以原图中点为中心，逆时针旋转180度并将长宽减半
#用getRotationMatrix2D求出变形矩阵M
#求出M后，warpAffine里依次传入原图，矩阵M和变形后的画布尺寸，就能得到新图片

rows,cols = im1.shape[:2]

# 这里的第一个参数为旋转中心，第二个为旋转角度，第三个为旋转后的缩放因子
# 可以通过设置旋转中心，缩放因子，以及窗口大小来防止旋转后超出边界的问题
M=cv2.getRotationMatrix2D((cols/2,rows/2),180,.5)                     #旋转缩放矩阵
print(type(M),M)

# 第三个参数是输出图像的尺寸中心
dst=cv2.warpAffine(im1,M,(2*cols,2*rows))                   #没有进行平移，但图片变小了看起来似乎平移了
cv2.imwrite('dst.jpg',dst)
#cv2.imshow('img',dst)





'''
仿射变换
在仿射变换中，原图中所有的平行线在结果图像中同样平行。
为了创建这个矩阵我们需要从原图像中找到三个点以及他们在输出图像中的位置。
然后cv2.getAffineTransform 会创建一个 2x3 的矩阵，最后这个矩阵会被传给函数 cv2.warpAffine。
来看看下面的例子，以及我选择的点（被标记为绿色的点）
'''

#获取三个点在平移前和平移后的坐标，用getAffineTransform计算平移矩阵M
pts1=np.float32([[50,50],[200,50],[50,200]])
pts2=np.float32([[10,100],[200,50],[100,250]])                    #三个点被扭曲（仿射变换）后的位置
M=cv2.getAffineTransform(pts1,pts2)                               #获取仿射变换的矩阵
dst=cv2.warpAffine(im1,M,(cols,rows))
plt.figure(12)
plt.subplot(121)
plt.imshow(im1)
plt.subplot(122)
plt.imshow(dst)
#plt.show()



'''
透视变换
对于视角变换，我们需要一个 3x3 变换矩阵。在变换前后直线还是直线。
要构建这个变换矩阵，你需要在输入图像上找 4 个点，以及他们在输出图
像上对应的位置。这四个点中的任意三个都不能共线。这个变换矩阵可以有
函数 cv2.getPerspectiveTransform() 构建。然后把这个矩阵传给函数
cv2.warpPerspective。
'''
#pts1是变换前的点，pts2是它们变换后对应的点，pts3用来测试是否取错值，可忽略
#getPerspectiveTransform用来获取透视矩阵，warpPerspective进行透视变换？
pts1 = np.float32([[589,317],[800,310],[800,439],[585,465]])
pts3=pts1.astype(int)
cv2.polylines(im1,[pts3],True,(0,0,255),3)
cv2.imshow('',im1)
pts2 = np.float32([[0,0],[300,0],[300,300],[0,300]])
M=cv2.getPerspectiveTransform(pts1,pts2)
dst=cv2.warpPerspective(im1,M,(300,300))
plt.subplot(121)
plt.imshow(im1)
plt.subplot(122)
plt.imshow(dst)
plt.show()

