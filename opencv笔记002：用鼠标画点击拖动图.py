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
    k = cv2.waitKey(1) 
    if k == ord('m'):                    # 切换模式
        mode = not mode
    elif k == 27:
        break

cv2.destroyAllWindows()
