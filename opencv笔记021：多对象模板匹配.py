'''
多对象的模板匹配
在前面的部分，我们在图片中搜素梅西的脸，而且梅西只在图片中出现了一次。假如你的目标对象只在图像中出现了很多次怎么办呢？
函数cv.imMaxLoc() 只会给出最大值和最小值。此时，我们就要使用阈值了。
在下面的例子中我们要经典游戏 Mario 的一张截屏图片中找到其中的硬币。
'''


import cv2
import numpy as np
from matplotlib import pyplot as plt

img_rgb = cv2.imread('2.jpg')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template  =img_gray[35:115,287:444]
w, h = template.shape[1],template.shape[0]
res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
threshold = 0.8

#umpy.where(condition[, x, y])
#Return elements, either from x or y, depending on condition.
#If only condition is given, return condition.nonzero().
loc = np.argwhere( res >= threshold)                            #大于阈值的标记表示出来
for pt in loc:                  
    cv2.rectangle(img_rgb, (pt[1],pt[0]), (pt[1] + w, pt[0] + h),(0,0,255), 2)
cv2.imshow('',img_rgb)
