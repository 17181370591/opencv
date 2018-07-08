#http://www.cnblogs.com/Undo-self-blog/p/8424056.html

import numpy as np
import cv2

#设置窗口大小
cv2.namedWindow('a',0)
cv2.resizeWindow('a',500,500)
cv2.imshow('a',img3)

# Create a black image
#这里一定要设置np.uint8，不然只要值大于0图片背景就是白色，原因不明。现在是灰色
img = np.ones((512,512,3), np.uint8)*166                    


#最后一个参数是线条的宽度，如果小于0则填充图片
#要画一条线，你只需要告诉函数这条线的起点和终点。我们下面会画一条从左上方到右下角的蓝色线段。
cv2.line(img,(0,0),(511,511),(255,0,0),5)


#要画一个矩形，你需要告诉函数的左上角顶点和右下角顶点的坐标。这次我们会在图像的右上角话一个绿色的矩形。
cv2.rectangle(img,(388,0),(510,128),(0,255,0),-3)


#要画圆的话，只需要指定圆形的中心点坐标和半径大小。我们在上面的矩形中画一个圆。
cv2.circle(img,(128,388),128,(0,0,255),1)


#画椭圆比较复杂，我们要多输入几个参数。一个参数是中心点的位置坐标。
#下一个参数是长轴和短轴的长度。椭圆沿逆时针方向旋转的角度。
#椭圆弧演顺时针方向起始的角度和结束角度，如果是 0 很 360，就是整个椭圆。查看cv2.ellipse() 可以得到更多信息。
#下面的例子是在图片的中心绘制3/4个椭圆。
cv2.ellipse(img,(256,256),(100,50),30,0,270,(0,255,255),2)


#画多边形，需要指点每个顶点的坐标。用这些点的坐标构建一个大小等于行数 X1X2 的数组，行数就是点的数目。
#这个数组的数据类型必须为 int32（我去掉了也没问题）。这里画一个黄色的具有四个顶点的多边形。
#需要注意pts的顺序会影响线条的顺序
pts = np.array([[10,5],[20,30],[50,10],[70,20]])
print(pts)
pts = pts.reshape((-1,1,2))
print(pts)
cv2.polylines(img,[pts],False,(0,255,255))


'''
　要在图片上绘制文字，你需要设置下列参数：
　　• 你要绘制的文字
　　• 你要绘制的位置
　　• 字体类型（通过查看 cv2.putText() 的文档找到支持的字体）
　　• 字体的大小
　　• 文字的一般属性如颜色，粗细，线条的类型等。为了更好看一点推荐使用linetype=cv2.LINE_AA。
在图像上绘制白色的 OpenCV。
'''
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img,'OpenCV',(256,499), font, 2,
            (255,255,255),2,cv2.LINE_AA)

#打开图片
cv2.imshow('',img)
