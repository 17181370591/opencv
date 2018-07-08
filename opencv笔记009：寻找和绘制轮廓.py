#http://www.cnblogs.com/Undo-self-blog/p/8438808.html

'''
 什么是轮廓
　　轮廓可以简单认为成将连续的点（连着边界）连在一起的曲线，具有相同、的颜色或者灰度。
  轮廓在形状分析和物体的检测和识别中很有用。
　　• 为了更加准确，要使用二值化图像。在寻找轮廓之前，要进行阈值化处理、或者 Canny 边界检测。
　　• 查找轮廓的函数会修改原始图像。如果你在找到轮廓之后还想使用原始图、像的话，你应该将原始图像存储到其他变量中。
　　• 在 OpenCV 中，查找轮廓就像在黑色背景中超白色物体。你应该记住，、要找的物体应该是白色而背景应该是黑色。
让我们看看如何在一个二值图像中查找轮廓：
　　函数 cv2.findContours() 有三个参数，第一个是输入图像，第二个是轮廓检索模式，第三个是轮廓近似方法。
  返回值有三个，第一个是图像，第二个是轮廓，第三个是（轮廓的）层析结构。轮廓（第二个返回值）是一个 Python列表，
  其中存储这图像中的所有轮廓。每一个轮廓都是一个 Numpy 数组，包含对象边界点（x，y）的坐标。
注意：我们后边会对第二和第三个参数，以及层次结构进行详细介绍。在那之前，例子中使用的参数值对所有图像都是适用的。
怎样绘制轮廓
　　函数 cv2.drawContours() 可以被用来绘制轮廓。它可以根据你提供的边界点绘制任何形状。它的第一个参数是原始图像，
  第二个参数是轮廓，一个 Python 列表。第三个参数是轮廓的索引（在绘制独立轮廓是很有用，当设置为 -1 时绘制所有轮廓）。
  接下来的参数是轮廓的颜色和厚度等。
在一幅图像上绘制所有的轮廓：
'''
import numpy as np
import cv2

im = cv2.imread('1.jpg')
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)        #转成灰度图
ret,thresh = cv2.threshold(imgray,166,255,0)        #转成二值图，注意阈值的取值
cv2.imshow('',thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()

#找轮廓和画轮廓
image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
img= cv2.drawContours(im, contours, -1, (0,255,0),2)      #-1会显示所有的轮廓，此时im已经被改变了
cv2.imshow('',img)
