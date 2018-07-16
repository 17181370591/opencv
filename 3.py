'''
霍夫变换
#https://blog.csdn.net/qq_37059483/article/details/77891698
OpenCV  中的霍夫变换
上面介绍的整个过程在 OpenCV 中都被封装进了一个函数：cv2.HoughLines()。
返回值就是（ρ,θ）。ρ 的单位是像素，θ 的单位是弧度。这个函数的第一个参
数是一个二值化图像，所以在进行霍夫变换之前要首先进行二值化，或者进行
Canny 边缘检测。第二和第三个值分别代表 ρ 和 θ 的精确度。第四个参数是
阈值，只有累加其中的值高于阈值时才被认为是一条直线，也可以把它看成能
检测到的直线的最短长度（以像素点为单位）。
'''
import cv2
import numpy as np
img = cv2.imread('2.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
lines = cv2.HoughLines(edges,1,np.pi/180,222)
lines=lines.reshape(-1,2)
print(lines.shape)
right=img.shape[1]
for z in lines:
    rho,theta=z
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    
    x1 = 0
    y1 = int(rho/b)
    x2 = right
    y2 = int((rho-x2*a)/b)
    print(x1,y1,x2,y2)
    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
    cv2.circle(img,(300,100),255,30)
    '''
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
    '''
    
cv2.imshow('houghlines3.jpg',img)
