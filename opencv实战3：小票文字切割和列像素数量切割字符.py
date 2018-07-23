#原贴：http://blog.51cto.com/boytnt/1686307
#https://blog.csdn.net/wx7788250/article/details/6013910
'''
第二个地址，提到了记录图片每一列的白点数量，然后根据这个切割图像，这种思路很有意思。
但他举的实例可以用简单方法切割，所以没有特意写一篇，只是补充在这里
'''

import matplotlib.pyplot as plt,cv2,numpy as np,pytesseract,PIL

a=cv2.imread('小票.jpg',1)
b=cv2.imread('小票.jpg',0)
ret, b = cv2.threshold(b,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

kernel = np.ones((1,15),np.uint8)        
#b= cv2.dilate(b,kernel,iterations = 1)                  #对方用了这个，我发现这个其实不需要
b=cv2.morphologyEx(b, cv2.MORPH_CLOSE, kernel)

i,contours,h= cv2.findContours(b,0,cv2.CHAIN_APPROX_NONE)

#下面生成的img是贴合每个字符的轮廓
#img= cv2.drawContours(a, contours, -1, (0,255,0),2)        
for cnt in contours:                                              #生成每块字符的轮廓矩形
    x,y,w,h = cv2.boundingRect(cnt)
    a = cv2.rectangle(a,(x,y),(x+w,y+h),(0,255,0),2)

cv2.imshow('',a)
