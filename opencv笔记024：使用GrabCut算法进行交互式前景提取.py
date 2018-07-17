#https://www.cnblogs.com/mikewolf2002/p/3330390.html
'''
现在我们进入 OpenCV 中的 grabcut 算法。OpenCV 提供了函数cv2.grabCut()。我们来先看看它的参数：

• img - 输入图像
• mask-掩模图像，用来确定那些区域是背景，前景，可能是前景/背景等。
可以设置为：cv2.GC_BGD,cv2.GC_FGD,cv2.GC_PR_BGD,cv2.GC_PR_FGD，或者直接输入 0,1,2,3 也行。
mask图像的值只能为下面下面4个值(PR，probably表示可能的)：
GC_BGD    = 0,  //背景
GC_FGD    = 1,  //前景 
GC_PR_BGD = 2,  //可能背景
GC_PR_FGD = 3   //可能前景 
• rect - 包含前景的矩形，格式为 (x,y,w,h)
• bdgModel, fgdModel - 算法内部使用的数组. 你只需要创建两个大
小为 (1,65)，数据类型为 np.float64 的数组。
• iterCount - 算法的迭代次数
• mode 可以设置为 cv2.GC_INIT_WITH_RECT 或 cv2.GC_INIT_WITH_MASK，
也可以联合使用。这是用来确定我们进行修改的方式，矩形模式或者掩模模式。

首先，我们来看使用矩形模式。加载图片，创建掩模图像，构建 bdgModel和 fgdModel。传入矩形参数。
让算法迭代 5 次。由于我们在使用矩形模式所以修改模式设置为 cv2.GC_INIT_WITH_RECT。
运行grabcut。算法会修改掩模图像，在新的掩模图像中，所有的像素被分为四类：
背景，前景，可能是背景/前景使用 4 个不同的标签标记（前面参数中提到过）。
然后我们来修改掩模图像，所有的 0 像素和 1 像素都被归为 0（例如背景），所有的 1 像素和 3 像素都被归为 1（前景）。
我们最终的掩模图像就这样准备好了。用它和输入图像相乘就得到了分割好的图像。

梅西的头发被我们弄没了！让我们来帮他找回头发。所以我们要在那里画一笔（设置像素为 1，肯定是前景）。
同时还有一些我们并不需要的草地。我们需要去除它们，我们再在这个区域画一笔（设置像素为 0，肯定是背景）。
现在可以象前面提到的那样来修改掩模图像了。实际上我是怎么做的呢？
我们使用图像编辑软件打开输入图像，添加一个图层，使用笔刷工具在需要的地方使用白色绘制（比如头发，鞋子，球等）；
使用黑色笔刷在不需要的地方绘制（比如，logo，草地等）。然后将其他地方用灰色填充，保存成新的掩码图像。
在 OpenCV 中导入这个掩模图像，根据新的掩码图像对原来的掩模图像进行编辑。
你也可以不使用矩形初始化，直接进入掩码图像模式。使用 2像素和 3 像素（可能是背景/前景）对矩形区域的像素进行标记。
然后象我们在第二个例子中那样对肯定是前景的像素标记为 1 像素。然后直接在掩模图像模式下使用 grabCut 函数。



import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('y5.jpg')                           #水果图
mask = np.zeros(img.shape[:2],np.uint8)
bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)                #初始化三个参数

#表示矩形的左上右下的坐标，矩形外都是背景，相当于参数0，矩形内可能是前景，相当于参数3。
#所以其实矩形模式就是将矩形内部改成3？
rect = (70,40,355,480)                              
# 函数的返回值是更新的 mask, bgdModel, fgdModel
cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)         #矩形模式

#下一句代码说明依旧有可能背景的部分，但不再继续运算，将可能背景转换成背景
mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
#运行下面三行代码程序就可以直接结束了，img是进行矩形模式提取的不经人工修改的图像
#img = img*mask2[:,:,np.newaxis]
#plt.imshow(img),plt.colorbar(),plt.show()
#cv2.imshow('',img)


#可以看到图像不完美，掺杂了一些背景，所以下面进行人工修改。
#img[450:470,130:150]明显是背景，所以在mask里设置0。不需要全部修改，只需取其中一部分修改即可，下面的mask模式一样。
#注意到这里mask是经过上面矩形模式修改后的mask，所以上面的grabCut不能省略
mask[450:470,130:150]=0
mask, bgdModel, fgdModel = cv2.grabCut(img,mask,None,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_MASK)
mask = np.where((mask==2)|(mask==0),0,1).astype('uint8')
#np.newaxis=None，所以下面也可以写img = img*mask[:,:,None]。关于numpy的乘法，最下面有注释
img = img*mask[:,:,np.newaxis]
cv2.imshow('',img)




#==========================================================================================
#上面是使用矩形模式后用mask模式进行修改，下面是直接使用mask模式。
#思路是把初始mask全部标记2（可修改的背景），然后把确认背景改成0，确认前景改成1。
#要改的地方很多，这里只改了一部分。运行速度闭比上面快，但是手动改的地方很多，适合结构简单的图形
'''
img = cv2.imread('y5.jpg')
mask = np.ones(img.shape[:2],np.uint8)
mask=mask*2
mask[0:100,300:500]=0
mask[0:260,0:60]=0
mask[140:390,140:280]=1
mask[150:240,400:490]=1

bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)
mask, bgdModel, fgdModel = cv2.grabCut(img,mask,None,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_MASK)

mask = np.where((mask==2)|(mask==0),0,1).astype('uint8')
img = img*mask[:,:,np.newaxis]
cv2.imshow('',img)
'''



#==========================================================================================
'''
numpy乘法的一些例子
>>> a=np.arange(24).reshape((4,3,2))
>>> a
array([[[ 0,  1],
        [ 2,  3],
        [ 4,  5]],

       [[ 6,  7],
        [ 8,  9],
        [10, 11]],

       [[12, 13],
        [14, 15],
        [16, 17]],

       [[18, 19],
        [20, 21],
        [22, 23]]])
>>> b=np.zeros_like(a)
>>> b
array([[[0, 0],
        [0, 0],
        [0, 0]],

       [[0, 0],
        [0, 0],
        [0, 0]],

       [[0, 0],
        [0, 0],
        [0, 0]],

       [[0, 0],
        [0, 0],
        [0, 0]]])
>>> b[:,:,1]=2
>>> a*b
array([[[ 0,  2],
        [ 0,  6],
        [ 0, 10]],

       [[ 0, 14],
        [ 0, 18],
        [ 0, 22]],

       [[ 0, 26],
        [ 0, 30],
        [ 0, 34]],

       [[ 0, 38],
        [ 0, 42],
        [ 0, 46]]])
>>> b=np.zeros_like(a)
>>> c=b[:,:,0]
>>> c[:1]=2
>>> c[:2]=3
>>> c=c.reshape((c.shape[0],c.shape[1],-1))
#c=c[:,:,None]
>>> c
array([[[0],
        [2],
        [3]],

       [[0],
        [2],
        [3]],

       [[0],
        [2],
        [3]],

       [[0],
        [2],
        [3]]])
>>> a*c
array([[[ 0,  0],
        [ 4,  6],
        [12, 15]],

       [[ 0,  0],
        [16, 18],
        [30, 33]],

       [[ 0,  0],
        [28, 30],
        [48, 51]],

       [[ 0,  0],
        [40, 42],
        [66, 69]]])
'''
