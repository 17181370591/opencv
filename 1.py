'''
思路是

1，事先做好棋子的模板：
棋子的模板由getkomapic制作，传入参数是差不多正好包裹住棋子的矩形截图，
这个函数会将此截图转换成相应的mask二值图，白色部分仅包含棋子，然后保存到电脑。

2，事先做好两种音符和再玩一局文字的模板：
因为棋子头部周围会低概率随机出现音符影响棋盘的定位，所以做好截图后做好模板，每次截图都进行模板匹配，
匹配度较高的值，替换该范围成等高的边界的值。同时也进行再玩一局文字匹配，
如果匹配度高（99%+）说明游戏结束了，main函数会返回0进行下一步处理。

3，其他预处理：
棋子部分使用模板匹配完全没问题；

棋盘部分：
由于棋盘似乎不会出现在337一下，所以只截取337以上的部分进行操作（对应变量to）；
由于背景颜色，棋盘颜色，阴影颜色和方向都会改变，似乎很难使用颜色进行处理，所以使用了canny，
canny的参数使用getCannyNum获取，内部用来滚动条实时测试效果，但一次只能测试一张图，
需要用多张图测试，实际上我是从游戏退出反馈的截图中进行测试。实际发现canny不能完美获取轮廓，
最终采用的参数会检测出背景的直线，不过可以很轻松的消除。

然后因为出现极点找到边缘点的bug，我把顶部100像素外，左右30像素外全部手动改0，后来发现bug原因是极限点取值时，
优先使用取极点附近某线的中值，如果某线上不存在点则会出现此bug，所以理论上这部分代码可以注释掉。

然后获取上左右3个极点。上极点优先使用下方2px的中值，返回0的话直接返回上极点。
左右极点优先使用内侧2px的上面第一个值（索引第一个，注意千万不能用中值，因为会把整个棋盘高度计入），报错的话返回原值。

由于不会处理阴影部分，而阴影部分只对左右极点之一产生影响，实际处理方法是找到距离中值更近的点取纵坐标即可，
缺点是容易收到棋子和棋子的音符干扰。棋子本身可以匹配后用边缘值（等于背景值）替换，
但音符可能出现大小不一和部分被遮盖的情况，即使使用了模板匹配依旧效果不佳，
所以匹配替换后再将棋子左右20px和上方50px的值替换成边缘值，
但是增加了消除棋盘有效范围而是棋盘中心上移的风险，不过效果还不错


====未完成



#然后将整个图大致分为阴影部分，背景部分和目标块部分，阴影部分随着背景又有变化，不好处理，背景部分取坐标0,0的点a，
#然后rgb值各-20得到b，a和b之间的都是背景；去掉这两部分，从上向下查询可得到目标块部分，
#目标块第一个点是上顶点，上顶点向左下走，走到横坐标变大时停止，此时的点是左顶点，
#分别取两个顶点在水平和垂直方向的交点，得到目标块的中点，但经常效果不好
'''

adb控制手机

查看屏幕大小  adb shell wm size

adb shell input swipe 100 100 200 200 300
从 100 100 经历300毫秒滑动到 200 200

adb shell input tap 500 1050        点击500，1050
'''


# -*- coding: utf-8 -*-
import os,math
import time,cv2
import numpy as np,random
import matplotlib.pyplot as plt


path1=r'C:\Users\Administrator\Desktop\111'
to=337

def getCannyNum(jpg='bug.jpg'):             #使用滚动条测试获取canny的两个参数
    img = cv2.imread(jpg,0)
    cv2.namedWindow('a')
    def nothing(x):
        pass

    cv2.createTrackbar('low','a',100,200,nothing)
    cv2.createTrackbar('high','a',0,255,nothing)

    img=img[:333,:]
    while 1:
        a=cv2.getTrackbarPos('low','a')
        b=cv2.getTrackbarPos('high','a')
        #print(a,b)
        edges = cv2.Canny(img,a,b)
        cv2.imshow('a',edges)
        cv2.waitKey(33)
        
        
        
#手动截图棋子后，处理掉背景，保存成koma1.jpg
def getkomapic(koma='koma.jpg'):
    im = cv2.imread(koma)
    thresh = cv2.imread(koma,0)
    ret,thresh1 = cv2.threshold(thresh,100,255,0)
    thresh1=cv2.bitwise_not(thresh1)
    image, contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    thresh1=cv2.drawContours(thresh1, contours, 0,255,-1)
    thresh1=cv2.drawContours(thresh1, contours, 2,255,-1)
    thresh1=np.uint8(thresh1/255)
    z=im*thresh1[:,:,None]
    cv2.imwrite('koma1.jpg',z)

#操作1对手机截图，保存成sdcard/autojump.png
#操作2将sdcard/autojump.png保存到电脑桌面，和操作2_1效果一样，注意2_1有个小数点表示当前路径

def pull_screenshot():
    os.system('adb shell screencap -p /sdcard/autojump.png')            #1
    #os.system('adb pull /sdcard/autojump.png .')                       #2_1
    os.system('adb pull /sdcard/autojump.png {}'.format(os.getcwd()))            #2
    img1=cv2.imread('autojump.png')
    img1=img1[300:1280,0:720]
    cv2.imwrite('autojump.png',img1)



#a,b分别是棋子到目标的横纵坐标的差值，z是长度，c是常数，将距离转换成时间

def sq(a,b,c=2.05):
    d=math.sqrt(a*a+b*b)
    z=round(d*c)
    return z



#获取棋子的中点,

def get_chess(img,img0):

    #img = cv2.imread('1.jpg',0)
    template =cv2.imread('koma1.jpg',0)
    w, h = template.shape[::-1]                 #获取元组列表反向元素的最便捷方法
    res = cv2.matchTemplate(img0,template,cv2.TM_CCOEFF)                  
    min_val, max_val, top_left, max_loc = cv2.minMaxLoc(res)
    bottom_right = (top_left[0] + w, top_left[1] + h)                
    cv2.rectangle(img,top_left, bottom_right, (0,255,255), 2)
    x=(top_left[0] + 27, top_left[1] + 126)
    cv2.circle(img,x,4,(0,255,255), -1)
    #cv2.imshow('',img)
    #cv2.waitKey(9999)
    return x[0],x[1],top_left,bottom_right


#获取目标块的中点
def get_pic(img,img0):
    #img=cv2.imread('autojump.png')
    #img0=cv2.imread('autojump.png',0)
    e = cv2.Canny(img0,5,0)[:to,:]
    e[e[:,1]==255]=0
    e[e[:,-1]==255]=0
#mark>>    
    e[:100]=0                                                      
    e[:,:30]=0                                         
    e[:,-30:]=0                                                
#mark<<    
    ds=np.argwhere(e==255)

    up1=ds[np.argmin(ds[:,0])]
    left1=ds[np.argmin(ds[:,1])]
    right1=ds[np.argmax(ds[:,1])]
    print(up1,left1,right1)
    
    up=np.int16(np.average(ds[ds[:,0]==up1[0]+2],axis=0))
    if up[0]==0:
        up=up1
    try:
        left=ds[np.argwhere(ds[:,1]==left1[1]+2)[0]][0]
    except Exception:
        left=left1
    try:
        right=ds[np.argwhere(ds[:,1]==right1[1]-2)[0]][0]
    except Exception:
        right=right1

 #mark  >> 
    #left,right=left1,right1                                                     
 #mark   <<
    cv2.circle(img,(up[1],up[0]),4,(0,0,255),-1)
    cv2.circle(img,(left[1],left[0]),4,(0,0,255),-1)
    cv2.circle(img,(right[1],right[0]),4,(0,0,255),-1)

    xx=up[1]
    a=abs(int(up[0]-left[0]))
    b=abs(int(up[0]-right[0]))
    yy=up[0]+min(a,b)
    
    cv2.circle(img,(xx,yy),4,(255,0,255),-1)
    return xx,yy,e

def delonpu(img,img0,onpu):
    while 1:
        w, h = onpu.shape[::-1]                 #获取元组列表反向元素的最便捷方法
        res = cv2.matchTemplate(img0,onpu,cv2.TM_CCOEFF_NORMED)                  
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val>0.7:
            print('max_val=',max_val)
            img[max_loc[1]:max_loc[1]+h,max_loc[0]:max_loc[0]+w]=img[max_loc[1]:max_loc[1]+h,0:w]
            img0[max_loc[1]:max_loc[1]+h,max_loc[0]:max_loc[0]+w]=img0[max_loc[1]:max_loc[1]+h,0:w]
        else:
            return

def main():
    temp1=np.zeros((980, 720, 3))
    temp2=np.zeros((to, 720, 3))
    temp3=np.zeros((980-to, 720, 3))
    name='{}.jpg'.format(time.strftime('%m-%d-%H-%M-%S',time.localtime(time.time())))
    while True:
        pull_screenshot()
        time.sleep(1)
        img=cv2.imread('autojump.png')
        img0=cv2.imread('autojump.png',0)           #下面的打开方法居然和这个有点不一样，这个图像信息更多
        #img0=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        
        delonpu(img,img0,onpu)
        delonpu(img,img0,onpu1)
        w1,w2,w3=img.shape


        
        bigpic=np.zeros((w1,w2*3+3,w3))
        bigpic[:,:w2,:]=temp1
        bigpic[:,3+w2:3+w2*2,:]=img
        bigpic[:to,3+w2*2:,:]=temp2
        bigpic[to:,3+w2*2:,:]=temp3
        cv2.imwrite(name,bigpic)


        res = cv2.matchTemplate(img0,aga,cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val>.9:
            print('游戏失败，即将重新开始')
            return 0
        mx,my,top_left,bottom_right=get_chess(img,img0)
        d1,d2=top_left
        d3,d4=bottom_right
 #mark>>>
        d2,d3,d4=d2-50,d3+20,d4+20                             
        if d1>20:            
            d1=d1-20        
        else:                
            d1=0             
 #mark<<<      
        img0[d2:d4,d1:d3]=img0[d2:d4,1].reshape((d4-d2,-1))
        '''
        cv2.imshow('',img0)
        cv2.waitKey(3333)
        cv2.destroyAllWindows()
        '''
        nx,ny,dst=get_pic(img,img0)
        dst1=np.repeat(dst.ravel(),3).reshape((to,720,3))
        dst2=np.repeat(img0[:980-to,:].ravel(),3).reshape((980-to,720,3))

        print('棋子的坐标是{},{}'.format(mx,my),'目标的坐标是{},{}'.format(nx,ny))
        
        z=sq(mx-nx,my-ny)
        x1=random.randrange(400,500)
        x2=random.randrange(400,500)
        x3=x1+random.randrange(-100,100)
        x4=x2+random.randrange(-100,100)
        cmd = 'adb shell input swipe {} {} {} {} {}'.format(x1,x2,x3,x4,z)
        os.system(cmd)
        time.sleep(3)       #2.5秒肯定不够
        temp1=img
        cv2.putText(dst1,r'{},{}/{},{}/{}'.format(mx,my,nx,ny,z),
                    (0,50), cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2,cv2.LINE_AA)
        temp2=dst1
        temp3=dst2


x=0
onpu =cv2.imread('konpu.jpg',0)
onpu1 =cv2.imread('konpu1.jpg',0)
aga=cv2.imread('kagain.jpg',0)
while 1:
    print('x=',x)
    if not x:
        time.sleep(3)
        x=1
        s='adb shell input tap 500 1050'
        #print(s)
        os.system(s)
    time.sleep(2)
    x=main()

