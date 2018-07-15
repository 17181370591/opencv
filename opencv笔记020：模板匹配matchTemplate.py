'''
模板匹配
在本节我们要学习：
1. 使用模板匹配在一幅图像中查找目标
2. 函数：cv2.matchTemplate()，cv2.minMaxLoc()
原理
模板匹配是用来在一副大图中搜寻查找模版图像位置的方法。OpenCV 为我们提供了函数：cv2.matchTemplate()。
和 2D 卷积一样，它也是用模板图像在输入图像（大图）上滑动，
并在每一个位置对模板图像和与其对应的输入图像的子区域进行比较。
OpenCV 提供了几种不同的比较方法（细节请看文档）。返回的结果是一个灰度图像，
每一个像素值表示了此区域与模板的匹配程度。
如果输入图像的大小是（WxH），模板的大小是（wxh），输出的结果的大小就是（W-w+1，H-h+1）。
当你得到这幅图之后，就可以使用函数cv2.minMaxLoc() 来找到其中的最小值和最大值的位置了。
第一个值为矩形左上角的点（位置），（w，h）为 moban 模板矩形的宽和高。这个矩形就是找到的模板区域了。
注意：如果你使用的比较方法是 cv2.TM_SQDIFF，最小值对应的位置才是匹配的区域。
我们看到 cv2.TM_CCORR 的效果不像我们想的那么好。
'''


import cv2
import numpy as np
from matplotlib import pyplot as plt


img = cv2.imread('2.jpg',0)
img2 = img.copy()
template =img2[35:115,287:444]
w, h = template.shape[::-1]
# All the 6 methods for comparison in a list
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED','cv2.TM_CCORR','cv2.TM_CCORR_NORMED',
           'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

for meth in methods:
    img = img2.copy()
    #exec 语句用来执行储存在字符串或文件中的 Python 语句。
    # 例如，我们可以在运行时生成一个包含 Python 代码的字符串，然后使用 exec 语句执行这些语句。
    #eval 语句用来计算存储在字符串中的有效 Python 表达式
    method = eval(meth)                                                      #遍历函数的方法！！！
    # Apply template Matching
    res = cv2.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # 使用不同的比较方法，对结果的解释不同
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:                      #带diff的方法要取最小值
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)                      #看来top_left就是左上角的顶点
    cv2.rectangle(img,top_left, bottom_right, 255, 2)
    plt.subplot(121),plt.imshow(res,cmap = 'gray')
    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(img,cmap = 'gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.suptitle(meth)
    plt.show()
