#http://www.cnblogs.com/Undo-self-blog/p/8447728.html

'''
OpenCV 中的 Harris 角点检测
　Open 中的函数 cv2.cornerHarris() 可以用来进行角点检测。参数如下：
　　• img - 数据类型为 float32 的输入图像。
　　• blockSize - 角点检测中要考虑的领域大小。
　　• ksize - Sobel 求导中使用的窗口大小
　　• k - Harris 角点检测方程中的自由参数，取值参数为 [0,04，0.06].
例子如下：
'''

import cv2
import numpy as np
from matplotlib import pyplot as plt

filename = '1.jpg'
img = cv2.imread(filename)
#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray=cv2.imread(filename,0)
gray = np.float32(gray)
# 输入图像必须是 float32 ，最后一个参数在 0.04 到 0.05 之间
dst = cv2.cornerHarris(gray,2,3,0.04)

#result is dilated for marking the corners, not important
#膨胀可以让点变大，不重要
dst = cv2.dilate(dst,None)

# Threshold for an optimal value, it may vary depending on the image.
img[dst>0.01*dst.max()]=[0,0,255]

cv2.imshow('dst',img)




#####################
'''
亚像素级精确度的角点
　　有时我们需要最大精度的角点检测。OpenCV 为我们提供了函数 cv2.cornerSubPix()，它可以提供亚像素级别的角点检测。
  下面是一个例子。首先我们要找到 Harris角点，然后将角点的重心传给这个函数进行修正。Harris 角点用红色像素标出，
  绿色像素是修正后的像素。在使用这个函数是我们要定义一个迭代停止条件。当迭代次数达到或者精度条件满足后迭代就会停止。
  我们同样需要定义进行角点搜索的邻域大小。
'''
img = cv2.imread(filename)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# find Harris corners
gray = np.float32(gray)
dst = cv2.cornerHarris(gray,2,3,0.04)
dst = cv2.dilate(dst,None)
ret, dst = cv2.threshold(dst,0.01*dst.max(),255,0)
dst = np.uint8(dst)

# find centroids
ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)

# define the criteria to stop and refine the corners
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
corners = cv2.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)

# Now draw them
res = np.hstack((centroids,corners))
res = np.int0(res)
img[res[:,1],res[:,0]]=[0,0,255]
img[res[:,3],res[:,2]] = [0,255,0]
cv2.imshow('a3',img)
cv2.imwrite('a3.jpg',img)






########################
'''
 Shi-Tomasi 角点检测 & 适合于跟踪的图像特征

目标
　本节我们将要学习：
　　• 另外一个角点检测技术：Shi-Tomasi 焦点检测
　　• 函数：cv2.goodFeatureToTrack()
OpenCV 提供了函数：cv2.goodFeaturesToTrack()。
这个函数可以帮我们使用 Shi-Tomasi 方法获取图像中 N 个最好的角点（如果你愿意的话，
也可以通过改变参数来使用 Harris 角点检测算法）。通常情况下，输入的应该是灰度图像。然后确定你想要检测到的角点数目。
再设置角点的质量水平，0到 1 之间。它代表了角点的最低质量，低于这个数的所有角点都会被忽略。
最后在设置两个角点之间的最短欧式距离。
根据这些信息，函数就能在图像上找到角点。所有低于质量水平的角点都会被忽略。然后再把合格角点按角点质量进行降序排列。
函数会采用角点质量最高的那个角点（排序后的第一个），然后将它附近（最小距离之内）的角点都删掉。
按着这样的方式最后返回 N 个最佳角点。在下面的例子中，我们试着找出 125 个最佳角点：
'''
num=125
img = cv2.imread(filename)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#gray = cv2.imread(filename，0)

corners = cv2.goodFeaturesToTrack(gray,num,0.01,10)
corners = np.int0(corners)

for i in corners:
    x,y = i.ravel()
    cv2.circle(img,(x,y),3,(0,0,255),-1)

cv2.imwrite('a3.jpg',img)
plt.imshow(img)
plt.show()
