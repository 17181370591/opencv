'''
统计直方图
　　现在我们知道什么是直方图了，那怎样获得一副图像的直方图呢？
　　OpenCV 和 Numpy 都有内置函数做这件事。在使用这些函数之前我们有必要想了解一下直方图相关的术语。

　　BINS：上面的直方图显示了每个灰度值对应的像素数。如果像素值为 0到 255，你就需要 256 个数来显示上面的直方图。
  但是，如果你不需要知道每一个像素值的像素点数目的，而只希望知道两个像素值之间的像素点数目怎么办呢？
  举例来说，我们想知道像素值在 0 到 15 之间的像素点的数目，接着是 16 到 31,....，240 到 255。
  我们只需要 16 个值来绘制直方图。OpenCVTutorials on histograms中例子所演示的内容。
那到底怎么做呢？你只需要把原来的 256 个值等分成 16 小组，取每组的总和。而这里的每一个小组就被成为 BIN。
第一个例子中有 256 个 BIN，第二个例子中有 16 个 BIN。在 OpenCV 的文档中用 histSize 表示 BINS。
　　DIMS：表示我们收集数据的参数数目。在本例中，我们对收集到的数据只考虑一件事：灰度值。所以这里就是 1。
　　RANGE：就是要统计的灰度值范围，一般来说为 [0，256]，也就是说所有的灰度值
使用 OpenCV 统计直方图 函数 cv2.calcHist 可以帮助我们统计一幅图像的直方图

可以帮助我们统计一幅图像的直方图。我们一起来熟悉一下这个函数和它的参数：
cv2.calcHist(images,channels,mask,histSize,ranges[,hist[,accumulate]])
　　1. images: 原图像（图像格式为 uint8 或 float32）。当传入函数时应该用中括号 [] 括起来，例如：[img]。
　　2. channels: 同样需要用中括号括起来，它会告诉函数我们要统计那幅图像的直方图。
        如果输入图像是灰度图，它的值就是 [0]；如果是彩色图像的话，
        传入的参数可以是 [0]，[1]，[2] 它们分别对应着通道 B，G，R。
　　3. mask: 掩模图像。要统计整幅图像的直方图就把它设为 None。但是如果你想统计图像某一部分的直方图的话，
        你就需要制作一个掩模图像，并使用它。（后边有例子）
　　4. histSize:BIN 的数目。也应该用中括号括起来，例如：[256]。
　　5. ranges: 像素值范围，通常为 [0，256]
'''


import cv2
import numpy as np
from matplotlib import pyplot as plt

#bins参数设置将range分为多少块，假设bins=64，那么每一块4个颜色值，这4个颜色值上的像素点的和就是图里的值。

pic='2.jpg'
bins=256
img = cv2.imread(pic,0)
color=['b','g','r']
# 别忘了中括号 [img],[0],None,[256],[0,256] ，只有 mask 没有中括号

#画灰色图片的直方图方法1：
hist = cv2.calcHist([img],[0],None,[bins],[0,256])          #获取直方图数据方法1
hist1,bins1 = np.histogram(img.ravel(),bins,[0,256])        #获取直方图数据方法2
hist2=np.bincount(img.ravel() ,minlength=bins)              #获取直方图数据方法3，这个比2快很多
plt.plot(hist)              
plt.xlim([0,256])
plt.show()                                                  #为什么这个画的是折线图？



#画灰色图片的直方图方法2：
img = cv2.imread(pic,0)
plt.hist(img.ravel(),256,[0,256])                           #直方图
plt.show()



#画rgb图片的直方图，为什么依旧是折线图？
img = cv2.imread(pic)                               
for i in range(3):
    hist=cv2.calcHist([img],[i],None,[bins],[0,256])
    plt.plot(hist,color=color[i])
plt.xlim([0,256])
plt.show()



#使用mask的直方图
#使用掩模
#要统计图像某个局部区域的直方图只需要构建一副掩模图像。将要统计的部分设置成白色，其余部分为黑色，
#就构成了一副掩模图像。然后把这个掩模图像传给函数就可以了。
#下面的代码中，掩模把灰度图一分为二，属于图像正好能拼接成第一个图
#如果想用cv2.calcHist，只需将img设置成使用掩模后的img即可

img = cv2.imread(pic,0)
mask=np.zeros_like(img)
yz=111
mask[img>yz]=255
mask1=cv2.bitwise_not(mask)
hist = cv2.calcHist([img],[0],mask,[bins],[0,256])
plt.plot(hist)
hist = cv2.calcHist([img],[0],mask1,[bins],[0,256])
plt.plot(hist)
plt.xlim([0,256])
plt.show()
