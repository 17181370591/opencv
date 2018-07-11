import cv2
import numpy as np
from matplotlib import pyplot as plt
'''
img = cv2.imread('4.jpg',0)
#flatten() 将数组变成一维
hist,bins = np.histogram(img.flatten(),256,[0,256])
# 计算累积分布图
cdf = hist.cumsum()
cdf_normalized = cdf * hist.max()/ cdf.max()
#plt.plot(cdf, color = 'g')
plt.plot(cdf_normalized, color = 'b')
plt.hist(img.flatten(),256,[0,256], color = 'r')
plt.xlim([0,256])
plt.legend(('cdf','histogram'), loc = 'upper left')
plt.show()

cdf_m = np.ma.masked_equal(cdf,0)
cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())
# 对被掩盖的元素赋值，这里赋值为 0
cdf= np.ma.filled(cdf_m1,0).astype('uint8')

img = cdf[img]
cv2.imwrite('a.jpg',img)
#a=cv2.calcHist([img2],[0],None,[256],[0,256])
'''
img = cv2.imread('1.jpg',0)
equ = cv2.equalizeHist(img)
#res = np.hstack((img,equ)) #stacking images side-by-side
#cv2.imwrite('a.jpg',res)
cv2.imwrite('a.jpg',equ)
