import cv2
import numpy as np
from matplotlib import pyplot as plt




p=5
img = cv2.imread('a1.jpg')





'''
2D  卷积
与以为信号一样，我们也可以对 2D 图像实施低通滤波（LPF），高通滤波（HPF）等。LPF 帮助我们去除噪音，模糊图像。
HPF 帮助我们找到图像的边缘。OpenCV 提供的函数 cv.filter2D() 可以让我们对一幅图像进行卷积操作。
下面我们将对一幅图像使用平均滤波器。下面是一个 5x5 的平均滤波器核：
操作如下：将核放在图像的一个像素 A 上，求与核对应的图像上 25（5x5）个像素的和，在取平均数
，用这个平均数替代像素 A 的值。重复以上操作直到将图像的每一个像素值都更新一边。代码如下，运行一下吧。
'''

kernel = np.ones((p,p),np.float32)/p/p
dst = cv2.filter2D(img,-1,kernel)





'''
高斯模糊
现在把卷积核换成高斯核（简单来说，方框不变，将原来每个方框的值是相等的，现在里面的值是符合高斯分布的，
方框中心的值最大，其余方框根据距离中心元素的距离递减，构成一个高斯小山包。
原来的求平均数现在变成求加权平均数，全就是方框里的值）。实现的函数是 cv2.GaussianBlur()。
我们需要指定高斯核的宽和高（必须是奇数）。以及高斯函数沿 X，Y 方向的标准差。
如果我们只指定了 X 方向的的标准差，Y 方向也会取相同值。如果两个标准差都是 0，那么函数会根据核函数的大小自己计算。
高斯滤波可以有效的从图像中去除高斯噪音。
'''

dst1=cv2.GaussianBlur(img,(p,p),0)






'''
中值模糊
顾名思义就是用与卷积框对应像素的中值来替代中心像素的值。这个滤波器经常用来去除椒盐噪声。
前面的滤波器都是用计算得到的一个新值来取代中心像素的值，而中值滤波是用中心像素周围（也可以使他本身）的值来取代他。
他能有效的去除噪声。卷积核的大小也应该是一个奇数。
'''

dst2=cv2.medianBlur(img,p)







'''
平均
这是由一个归一化卷积框完成的。他只是用卷积框覆盖区域所有像素的平均值来代替中心元素。
可以使用函数 cv2.blur() 和 cv2.boxFilter() 来完这个任务。可以同看查看文档了解更多卷积框的细节。
我们需要设定卷积框的宽和高。下面是一个 3x3 的归一化卷积框：
'''

dst3 = cv2.blur(img,(p,p))








'''
双边滤波
函数 cv2.bilateralFilter() 能在保持边界清晰的情况下有效的去除噪音。但是这种操作与其他滤波器相比会比较慢。
我们已经知道高斯滤波器是求中心点邻近区域像素的高斯加权平均值。这种高斯滤波器只考虑像素之间的空间关系，
而不会考虑像素值之间的关系（像素的相似度）。所以这种方法不会考虑一个像素是否位于边界。
因此边界也会别模糊掉，而这正不是我们想要。双边滤波在同时使用空间高斯权重和灰度值相似性高斯权重。
空间高斯函数确保只有邻近区域的像素对中心点有影响，
灰度值相似性高斯函数确保只有与中心像素灰度值相近的才会被用来做模糊运算。
所以这种方法会确保边界不会被模糊掉，因为边界处的灰度值变化比较大。
'''
#9 邻域直径，两个 75 分别是空间高斯函数标准差，灰度值相似性高斯函数标准差
blur1 = cv2.bilateralFilter(img,9,75,75)





plt.subplot(231),plt.imshow(img),plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(232),plt.imshow(dst),plt.title('2D  juanji')
plt.xticks([]), plt.yticks([])
plt.subplot(233),plt.imshow(dst1),plt.title('gaosi')
plt.xticks([]), plt.yticks([])
plt.subplot(234),plt.imshow(dst2),plt.title('zhongzhi lvbo')
plt.xticks([]), plt.yticks([])
plt.subplot(235),plt.imshow(dst3),plt.title('blur')
plt.xticks([]), plt.yticks([])
plt.subplot(236),plt.imshow(blur1),plt.title('shuangbian lvbo')
plt.xticks([]), plt.yticks([])
plt.show()
