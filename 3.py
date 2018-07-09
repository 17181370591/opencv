import cv2
import numpy as np
def f(contours):                                                #求轮廓列表里点最多的轮廓
    x=0
    p=0
    for i in range(len(contours)):
        if len(contours[i])>p:
            x=i
            p=len(contours[i])
    return x



yz=122
img1 = cv2.imread('4.jpg')
img = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
img=cv2.bitwise_not(img)
ret,thresh = cv2.threshold(img,yz,255,0)


kernel = np.ones((15,15),np.uint8)
thresh=cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
thresh=cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)             #各种初始化


image,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,3)          #获取轮廓列表
xx=f(contours)                                  
cnt = contours[xx]
hull = cv2.convexHull(cnt) 
img1=cv2.drawContours(img1,[hull],-1,(255,0,0),5)
cv2.imwrite('a.jpg',img1)
'''
Point Polygon Test
求解图像中的一个点到一个对象轮廓的最短距离。如果点在轮廓的外部，
返回值为负。如果在轮廓上，返回值为 0。如果在轮廓内部，返回值为正。

下面我们以点（50，50）为例：

dist = cv2.pointPolygonTest(cnt,(50,50),True)
此函数的第三个参数是 measureDist。如果设置为 True，就会计算最短距离。如果是 False，只会判断这个点与轮廓之间的位置关系（返回值为+1，-1，0）。

注意：如果你不需要知道具体距离，建议你将第三个参数设为 False，这样速度会提高 2 到 3 倍。
'''
dist = cv2.pointPolygonTest(cnt,(50,50),False)
#求中点到轮廓的距离
a=hull[hull[:,:,0].argmax(),:,:]/2+hull[hull[:,:,0].argmin(),:,:]/2
a=np.int0(a)
dist=cv2.pointPolygonTest(cnt,tuple(a.tolist()[0]),1)

'''
 形状匹配
　　函数 cv2.matchShape() 可以帮我们比较两个形状或轮廓的相似度。如果返回值越小，匹配越好。它是根据 Hu 矩来计算的。文档中对不同的方法都有解释。
我们试着将下面的图形进行比较
'''
ret1 = cv2.matchShapes(cnt,cnt,1,0.0)
ret2 = cv2.matchShapes(cnt1,cnt2,1,0.0)
