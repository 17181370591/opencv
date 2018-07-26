#http://www.cnblogs.com/Undo-self-blog/p/8439149.html

'''
直方图反向投影

它可以用来做图像分割，或者在图像中找寻我们感兴趣的部分。简单来说，它会输出与输入图像（待搜索）同样大小的图像，
其中的每一个像素值代表了输入图像上对应点属于目标对象的概率。用更简单的话来解释，
输出图像中像素值越高（越白）的点就越可能代表我们要搜索的目标（在输入图像所在的位置）。
这是一个直观的解释。直方图投影经常与 camshift算法等一起使用。
我们应该怎样来实现这个算法呢？首先我们要为一张包含我们要查找目标的图像创建直方图（在我们的示例中，
我们要查找的是草地，其他的都不要）。我们要查找的对象要尽量占满这张图像（换句话说，
这张图像上最好是有且仅有我们要查找的对象）。最好使用颜色直方图，
因为一个物体的颜色要比它的灰度能更好的被用来进行图像分割与对象识别。
接着我们再把这个颜色直方图投影到输入图像中寻找我们的目标，
也就是找到输入图像中的每一个像素点的像素值在直方图中对应的概率，这样我们就得到一个概率图像，
最后设置适当的阈值对概率图像进行二值化，就这么简单
'''
#在target里面找roi相似的部分，这里roi直接从target里取一部分。
#先将这两个图hsv化，对roi求直方图的目的是calcBackProject需要这个参数，
#roihist是roi的直方图，然后归一化并赋值给roilist，
#灰度图dst2就是反向投影的结果（反向投影到这一步就完了，图片白色部分表示比较像roi）。
#用2d卷积成dst1是为了填充dst2，也可以用闭运算填充成dst1，
#填充后转二值图，再转rgb图后与原图位并运算


import cv2
import numpy as np
from matplotlib import pyplot as plt


target = cv2.imread('o.jpg')
roi=target[30:50,240:260]
hsv = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
hsvt = cv2.cvtColor(target,cv2.COLOR_BGR2HSV)
# calculating object histogram
roihist = cv2.calcHist([hsv],[0, 1], None, [180, 256], [0, 180, 0, 256] )
# normalize histogram and apply backprojection
# 归一化：原始图像，结果图像，映射到结果图像中的最小值，最大值，归一化类型
#cv2.NORM_MINMAX 对数组的所有值进行转化，使它们线性映射到最小值和最大值之间
# 归一化之后的直方图便于显示，归一化之后就成了 0 到 255 之间的数了。
cv2.normalize(roihist,roihist,0,255,cv2.NORM_MINMAX)
dst2 = cv2.calcBackProject([hsvt],[0,1],roihist,[0,180,0,256],1)



# Now convolute with circular disc
# 此处卷积可以把分散的点连在一起
x=7
disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(x,x))     #使用椭圆核心
dst=cv2.filter2D(dst2,-1,disc)                                #用2d卷积填充
# threshold and binary AND
ret,thresh = cv2.threshold(dst,50,255,0)                      #灰度图转二值图（二值图是灰度图的一种）
# 别忘了是三通道图像，因此这里使用 merge 变成 3 通道
thresh = cv2.merge((thresh,thresh,thresh))                    #灰度图进行位并运算转换成rgb图      
res = cv2.bitwise_and(target,thresh)


ke=np.ones((x,x))                                              #和上一段作用一样，用来测试比原酸填充的效果
dst1=cv2.morphologyEx(dst2,cv2.MORPH_CLOSE,ke)                 #用闭运算填充
ret,dst1 = cv2.threshold(dst1,50,255,0)   
thresh1 = cv2.merge((dst1,dst1,dst1))                          #填充完是灰度图，要进行位并运算要转换成rgb图
res1 = cv2.bitwise_and(target,thresh1)


       
plt.subplot(2,2,1)
plt.imshow(target)
plt.subplot(2,2,2)
plt.imshow(thresh)
plt.subplot(2,2,3)
plt.imshow(res)
plt.subplot(2,2,4)
plt.imshow(res1)
plt.show()





'''
关于归一化：
>>> a=np.array([[0,0],[1,2],[2,3]])
>>> b=np.zeros_like(a)
>>> c=cv2.normalize(a,b,0,255,cv2.NORM_MINMAX)
#可以直接c=cv2.normalize(a,a,0,255,cv2.NORM_MINMAX)
>>> a
array([[0, 0],
       [1, 2],
       [2, 3]])
>>> b
array([[  0,   0],
       [ 85, 170],
       [170, 255]])
>>> c
array([[  0,   0],
       [ 85, 170],
       [170, 255]])
'''
