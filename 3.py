import numpy as np
import cv2
from matplotlib import pyplot as plt
img = cv2.imread('y4.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
#ret, thresh = cv2.threshold(gray,160,255,cv2.THRESH_BINARY_INV)



'''
现在我们要去除图像中的所有的白噪声。这就需要使用形态学中的开运算。
为了去除对象上小的空洞我们需要使用形态学闭运算。所以我们现在知道靠近
对象中心的区域肯定是前景，而远离对象中心的区域肯定是背景。而不能确定
的区域就是硬币之间的边界。
所以我们要提取肯定是硬币的区域。腐蚀操作可以去除边缘像素。剩下就
可以肯定是硬币了。当硬币之间没有接触时，这种操作是有效的。但是由于硬
币之间是相互接触的，我们就有了另外一个更好的选择：距离变换再加上合适
的阈值。接下来我们要找到肯定不是硬币的区域。这是就需要进行膨胀操作了。
膨胀可以将对象的边界延伸到背景中去。这样由于边界区域被去处理，我们就
可以知道那些区域肯定是前景，那些肯定是背景。
剩下的区域就是我们不知道该如何区分的了。这就是分水岭算法要做的。
这些区域通常是前景与背景的交界处（或者两个前景的交界）。我们称之为边
界。从肯定是不是背景的区域中减去肯定是前景的区域就得到了边界区域。
'''
# noise removal
kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel,iterations = 2)


# sure background area
#sure_bg的黑色部分一定是背景
sure_bg = cv2.dilate(opening,kernel,iterations=3)


# Finding sure foreground area
# 距离变换的基本含义是计算一个图像中非零像素点到最近的零像素点的距离，也就是到零像素点的最短距离
# 个最常见的距离变换算法就是通过连续的腐蚀操作来实现，腐蚀操作的停止条件是所有前景像素都被完全
# 腐蚀。这样根据腐蚀的先后顺序，我们就得到各个前景像素点到前景中心??像素点的
# 距离。根据各个像素点的距离值，设置为不同的灰度值。这样就完成了二值图像的距离变换
#cv2.distanceTransform(src, distanceType, maskSize)
# 第二个参数 0,1,2 分别表示 CV_DIST_L1, CV_DIST_L2 , CV_DIST_C
dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)

#sure_fg的白色部分一定是前景
ret, sure_fg = cv2.threshold(dist_transform,.7*dist_transform.max(),255,0)
# Finding unknown region
sure_fg = np.uint8(sure_fg)



unknown = cv2.subtract(sure_bg,sure_fg)
u1=cv2.subtract(opening,sure_fg)


'''
如结果所示，在阈值化之后的图像中，我们得到了肯定是硬币的区域，而
且硬币之间也被分割开了。（有些情况下你可能只需要对前景进行分割，而不需
要将紧挨在一起的对象分开，此时就没有必要使用距离变换了，腐蚀就足够了。
170
www.linuxidc.com
当然腐蚀也可以用来提取肯定是前景的区域。）
现在知道了那些是背景那些是硬币了。那我们就可以创建标签（一个与原
图像大小相同，数据类型为 in32 的数组），并标记其中的区域了。对我们已经
确定分类的区域（无论是前景还是背景）使用不同的正整数标记，对我们不确
定的区域使用 0 标记。我们可以使用函数 cv2.connectedComponents()
来做这件事。它会把将背景标记为 0，其他的对象使用从 1 开始的正整数标记。
但是，我们知道如果背景标记为 0，那分水岭算法就会把它当成未知
区域了。所以我们想使用不同的整数标记它们。而对不确定的区域（函数
cv2.connectedComponents 输出的结果中使用 unknown 定义未知区
域）标记为 0。
'''
# Marker labelling
ret, markers1 = cv2.connectedComponents(sure_fg)
#markers1=np.zeros((480,512))
# Add one to all labels so that sure background is not 0, but 1
markers = markers1+1
# Now, mark the region of unknown with zero
markers[unknown==255] = 0
#markers[u1==255] = 0
'''
结果使用 JET 颜色地图表示。深蓝色区域为未知区域。肯定是硬币的区域
使用不同的颜色标记。其余区域就是用浅蓝色标记的背景了。
现在标签准备好了。到最后一步：实施分水岭算法了。标签图像将会被修
改，边界区域的标记将变为 -1.
'''

markers3 = cv2.watershed(img,markers)
img[markers3 == -1] = [255,0,0]

def no(m,n):
    c=np.zeros_like(m)
    c=cv2.normalize(m,c,0,255,cv2.NORM_MINMAX)
    cv2.imwrite(n,c)


no(thresh,'mthresh.jpg')
no(opening,'mopening.jpg')
no(sure_bg,'msure_bg.jpg')
no(dist_transform,'mdist_transform.jpg')
no(sure_fg,'msure_fg.jpg')
no(unknown,'munknown.jpg')
no(u1,'mu1.jpg')
no(markers1,'markers1.jpg')
no(markers,'markers.jpg')
no(markers3,'markers3.jpg')

cv2.imshow('img',img)

