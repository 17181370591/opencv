#http://www.cnblogs.com/Undo-self-blog/p/8424056.html

import cv2
import numpy as np

drawing = False     #画图模式，防止鼠标经过就画图
mode = True         #画矩形模式，按m切换，可以切换成画圆模式
ix,iy = -1,-1       #随便给个初始值



def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,mode

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            if mode == True:                
                #cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
                pass
            else:
                cv2.circle(img,(x,y),5,(0,0,255),-1)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if mode == True:
            cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),1)
        else:
            cv2.circle(img,(x,y),5,(0,0,255),-1)

            
img = np.zeros((512,512,3), np.uint8)

#下面这两句代码可以都放进while 1里，这样就相当于不停的创建窗口并绑定函数，
#窗口有鼠标操作后就会在img上作画，而img的内容不受窗口影响，生成新窗口后继续在新窗口上展示。

#先创建窗口，这里这句不能省略
cv2.namedWindow('image')  
#需要注意：这里窗口对象没有使用变量，而是单纯使用了字符串，推测这个库内部有将字符串到串口对象的映射
cv2.setMouseCallback('image',draw_circle)

while 1:
    cv2.imshow('image',img)
    k = cv2.waitKey(1) &0xFF
    if k == ord('m'):                    # 切换模式
        mode = not mode
    elif k == 27:
        break

cv2.destroyAllWindows()

#=======================================================================
#test2

import numpy as np
import cv2,time
from matplotlib import pyplot as plt

im1=cv2.imread('1.jpg')
cv2.namedWindow('a',0)
cv2.resizeWindow('a',800,600)

def nn(x):
    pass

max_=100
cv2.createTrackbar('r','a',0,max_,nn)
cv2.createTrackbar('g','a',0,max_,nn)
cv2.createTrackbar('b','a',0,max_,nn)



while 1:
    r=cv2.getTrackbarPos('r','a')
    g=cv2.getTrackbarPos('g','a')
    b=cv2.getTrackbarPos('b','a')
    L=(r/100,g/100,b/100)
    im=im1.copy()
    for i in range(3):
      im[:,:,i]=np.uint8(im1[:,:,i]*L[i])

    cv2.imshow('a',im)
    cv2.waitKey(20)&0xFF



