import cv2
import numpy as np
from matplotlib import pyplot as plt


'''
简单阈值
与名字一样，这种方法非常简单。但像素值高于阈值时，我们给这个像素赋予一个新值（可能是白色），
否则我们给它赋予另外一种颜色（也许是黑色）。这个函数就是 cv2.threshhold()。这个函数的第一个参数就是原图像，
原图像应该是灰度图。第二个参数就是用来对像素值进行分类的阈值。
第三个参数就是当像素值高于（有时是小于）阈值时应该被赋予的新的像素值。
OpenCV提供了多种不同的阈值方法，这是有第四个参数来决定的。这些方法包括：
'''

#五种不同的二值化操作
img=cv2.imread('a1.jpg',0)
ret,thresh1=cv2.threshold(img,127,255,cv2.THRESH_BINARY)
ret,thresh2=cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)

#下面行的255似乎没用。t3的上限是127，后两个把符合条件的改成0
#t3使用plt显示不正常，127的地方显示成255
ret,thresh3=cv2.threshold(img,127,255,cv2.THRESH_TRUNC)
ret,thresh4=cv2.threshold(img,127,255,cv2.THRESH_TOZERO)
ret,thresh5=cv2.threshold(img,127,255,cv2.THRESH_TOZERO_INV)
titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]
for i in range(6):
    plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()




'''
自适应阈值
在前面的部分我们使用是全局阈值，整幅图像采用同一个数作为阈值。当时这种方法并不适应与所有情况，
尤其是当同一幅图像上的不同部分的具有不同亮度时。这种情况下我们需要采用自适应阈值。
此时的阈值是根据图像上的每一个小区域计算与其对应的阈值。因此在同一幅图像上的不同区域采用的是不同的阈值，
从而使我们能在亮度不同的情况下得到更好的结果。这种方法需要我们指定三个参数，返回值只有一个。
• Adaptive Method- 指定计算阈值的方法。
– cv2.ADPTIVE_THRESH_MEAN_C：阈值取自相邻区域的平
均值
– cv2.ADPTIVE_THRESH_GAUSSIAN_C：阈值取值相邻区域
的加权和，权重为一个高斯窗口。
• Block Size - 邻域大小（用来计算阈值的区域大小），因为要取中间值所以要设置奇数。
• C - 这就是是一个常数，阈值就等于的平均值或者加权平均值减去这个常
数。
#如果不设置c，当出现11个点都相同的情况下，会全部显示黑色。其他情况可自行推理
'''


img=cv2.imread('a1.jpg',0)
# 中值滤波，可以有效的消除噪声
img = cv2.medianBlur(img,5)
ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
#11 为 Block size, 2 为 C 值
th2 = cv2.adaptiveThreshold(img,55,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,0)
th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
titles = ['Original Image', 'Global Thresholding (v = 127)',
          'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
images = [img, th1, th2, th3]
for i in range(4):
    plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()




'''
Otsu’s  二值化
在第一部分中我们提到过 retVal，当我们使用 Otsu 二值化时会用到它。那么它到底是什么呢？
在使用全局阈值时，我们就是随便给了一个数来做阈值，那我们怎么知道我们选取的这个数的好坏呢？答案就是不停的尝试。
如果是一副双峰图像（简单来说双峰图像是指图像直方图中存在两个峰）呢？
我们岂不是应该在两个峰之间的峰谷选一个值作为阈值？这就是 Otsu 二值化要做的。
简单来说就是对一副双峰图像自动根据其直方图计算出一个阈值。（对于非双峰图像，这种方法得到的结果可能会不理想）。
这里用到到的函数还是 cv2.threshold()，但是需要多传入一个参数（flag）：cv2.THRESH_OTSU。这时要把阈值设为 0。
然后算法会找到最优阈值，这个最优阈值就是返回值 retVal。如果不使用 Otsu 二值化，返回的retVal 值与设定的阈值相等。
下面的例子中，输入图像是一副带有噪声的图像。第一种方法，我们设127 为全局阈值。
第二种方法，我们直接使用 Otsu 二值化。第三种方法，我们首先使用一个 5x5 的高斯核除去噪音，然后再使用 Otsu 二值化。
看看噪音去除对结果的影响有多大吧。
'''


img=cv2.imread('a1.jpg',0)
# global thresholding
ret1,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
# Otsu's thresholding
ret2,th2 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
# Otsu's thresholding after Gaussian filtering
# （ 5,5 ）为高斯核的大小， 0 为标准差
blur = cv2.GaussianBlur(img,(5,5),0)
# 阈值一定要设为 0 ！
ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

imgg = cv2.medianBlur(img,5)                                        #也试试中值滤波
ret4,th4 = cv2.threshold(imgg,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# plot all the images and their histograms
images = [img, 0, th1,img, 0, th2,blur, 0, th3, imgg, 0, th4]
titles = ['Original Noisy Image','Histogram','Global Thresholding (v=127)',
                'Original Noisy Image','Histogram',"Otsu's Thresholding",
                'Gaussian filtered Image','Histogram',"Otsu's Thresholding",
                  'zhongzhi lvbo','HHH',"Otsu's Thresholding"]
# 这里使用了 pyplot 中画直方图的方法， plt.hist, 要注意的是它的参数是一维数组
# 所以这里使用了（ numpy ） ravel 方法，将多维数组转换成一维，也可以使用 flatten 方法
#ndarray.flat 1-D iterator over an array.
#ndarray.flatten 1-D array copy of the elements of an array in row-major order.
x=4
for i in range(x):
    y=i*3
    print(y,type(y))
    plt.subplot(x,3,y+1)
    plt.imshow(images[i*3])
    plt.title(titles[i*3]), plt.xticks([]), plt.yticks([])
    plt.subplot(x,3,y+2),plt.hist(images[i*3].ravel(),256)
    plt.title(titles[i*3+1]), plt.xticks([]), plt.yticks([])
    plt.subplot(x,3,y+3),plt.imshow(images[i*3+2],'gray')
    plt.title(titles[i*3+2]), plt.xticks([]), plt.yticks([])

plt.show()


