import cv2
import numpy as np
from matplotlib import pyplot as plt
def f(contours):                                                #求轮廓列表里点最多的轮廓
    x=0
    p=0
    for i in range(len(contours)):
        if len(contours[i])>p:
            x=i
            p=len(contours[i])
    return x

pic='2.jpg'
bins=256
img = cv2.imread(pic,0)
color=['b','g','r']
# 别忘了中括号 [img],[0],None,[256],[0,256] ，只有 mask 没有中括号
hist = cv2.calcHist([img],[0],None,[bins],[0,256])
hist1,bins1 = np.histogram(img.ravel(),bins,[0,256])
hist2=np.bincount(img.ravel() ,minlength=bins)
plt.plot(hist)
plt.xlim([0,256])
plt.show()

img = cv2.imread(pic)
for i in range(3):
    hist=cv2.calcHist([img],[i],None,[bins],[0,256])
    plt.plot(hist,color=color[i])
plt.xlim([0,256])
plt.show()

img = cv2.imread(pic,0)
plt.hist(img.ravel(),256,[0,256])
plt.show()

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
