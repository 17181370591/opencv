#http://www.cnblogs.com/Undo-self-blog/p/8438808.html
import numpy as np
import cv2


def f(contours):                                                #求轮廓列表里点最多的轮廓
    x=0
    p=0
    for i in range(len(contours)):
        if len(contours[i])>p:
            x=i
            p=len(contours[i])
    return x


def sh(img1,b='a'):                                    #展示图片
    cv2.namedWindow(b,0)
    cv2.resizeWindow(b,500,500)
    cv2.imshow(b,img1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    
def ra(a,b):                                        #计算a，b两点的距离
    return np.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)




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
hull = cv2.convexHull(contours[xx])                                          #寻找凸包


img1 = cv2.imread('4.jpg')
img3= cv2.drawContours(img1, [hull], -1, (0,0,255),5)
sh(img3,'tu bao tu')


img1 = cv2.imread('4.jpg')                                   
rect= cv2.minAreaRect(hull)        #[contours[xx]]                 #寻找包围凸包的最小不旋转矩形
box = np.int0(cv2.boxPoints(rect))                                  #取整数
img1 = cv2.drawContours(img1,[box],0,(0,255,255),5)                 #画图
w,h=ra(box[0],box[1]),ra(box[2],box[1])                         #获取矩形的宽和高，顺序可能是反的，没验证




#边界矩形的宽高比
aspect_ratio = float(w)/h
print('边界矩形的宽高比：',aspect_ratio)



#轮廓面积与边界矩形面积的比
area = cv2.contourArea(contours[xx])            #计算轮廓面积
extent = float(area)/(w*h)
print('轮廓面积与边界矩形面积的比：',extent)




#轮廓面积与凸包面积的比
area1 = cv2.contourArea(hull)
solidity = float(area)/float(area1)
print('轮廓面积与凸包面积的比：',solidity)



#与轮廓面积相等的圆形的直径
equi_diameter = np.sqrt(4*area/np.pi)
print('与轮廓面积相等的圆形的直径：',equi_diameter)
cv2.circle(img1,tuple(np.int0(rect[0])),int(equi_diameter/2),(0,0,255),5)       #把圆画出来作验证



#下面这个方法意义不明，求出来的长轴和短轴似乎要除以2才对
#对象的方向，下面的方法还会返回长轴和短轴的长度，
#里面的points类型要求是numpy.array（[[x,y],[x1,y1]...]） 并不是把所有点都包括在椭圆里面，
#而是拟合出一个椭圆尽量使得点都在圆上
ellipse1= cv2.fitEllipse(contours[xx])
print(ellipse1)



#下面这个方法可以制作一个轮廓对应的mask
#掩模和像素点.有时我们需要构成对象的所有像素点，我们可以这样做：
mask = np.zeros(img1.shape[:2],np.uint8)                #[:2]是因为制作mask只需要用灰度图
# 最后一个参数一定是-1, 绘制填充的的轮廓,不然会表示轮廓的宽度而不是填充
cv2.drawContours(mask,[contours[xx][:,:,:2]],-1,255,-1)
#下面能得到mask所有像素点的numpy.array对象
pixelpoints = np.transpose(np.nonzero(mask))


'''
最大值和最小值及它们的位置，我们可以使用掩模图像得到这些参数。
这个方法寻找img1的mask范围里，灰度值最小和最大的点灰度值和坐标。。。
'''
img1 = cv2.imread('4.jpg',0)
mask = np.zeros(img1.shape,np.uint8)
a=cv2.drawContours(mask,[contours[xx]],-1,(255,255,255),-1)
min_val, max_val, min_loc, max_loc=cv2.minMaxLoc(img1,mask = mask)




#平均颜色及平均灰度：
mean_val = cv2.mean(img1,mask = mask)




'''
极点：一个对象最上面，最下面，最左边，最右边的点。注释里是我的写法
cnt=contours[xx].reshape((-1,2))
leftmost = cnt[cnt[:,0].argmin()]
rightmost=cnt[cnt[:,0].argmax()]
topmost=cnt[cnt[:,1].argmin()]
bottommost=cnt[cnt[:,1].argmax()]
'''
cnt=contours[xx]
leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])



sh(img1,'ju xing bian jie')


