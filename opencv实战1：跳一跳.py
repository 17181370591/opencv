'''
最好成绩1w7左右，不小心退出了，上个版本貌似不到1k。
无法应对作弊检测，通过自杀堆高平均值和故意偏移中点都被查出。
用其他作弊方法可以发现如果跳出的值低于自己的最高值，是不会进行作弊检测的。
#抓包分析：https://zhuanlan.zhihu.com/p/32711402?utm_source=wechat_session&utm_medium=social
思路是：

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
但是增加了消除棋盘有效范围而是棋盘中心上移的风险，不过效果还不错。

其他的见代码注释
'''

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
import matplotlib.pyplot as plt,pytesseract


path1=r'C:\Users\Administrator\Desktop\111'
to=337


def score(a):                               #获取当前分数
    a=a[-70:]
    #cv2.namedWindow('a',0)
    #cv2.resizeWindow('a',1200,600)    
    #cv2.imshow('a',a)
    r= pytesseract.image_to_string(a,lang='all',config='-psm 7')
    try:
        return int(r)
    except Exception:
        return 0
    
   
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
#实际案例中，contours含有4个元素，分别是棋子头部和身体的外轮廓，和棋子头部身体内部空缺部分的外轮廓，
#所以填充头部和身体的外轮廓就可以获得棋子的mask
def getkomapic(koma='koma.jpg'):
    im = cv2.imread(koma)
    thresh = cv2.imread(koma,0)
    ret,thresh1 = cv2.threshold(thresh,100,255,0)
    thresh1=cv2.bitwise_not(thresh1)
    
    image, contours, hierarchy = cv2.findContours(thresh1,0,cv2.CHAIN_APPROX_NONE)
    thresh1=cv2.drawContours(thresh1, contours, -1,255,-1)
    #以前用下三行代码，其实取外边轮廓用上面两行要好很多
    '''
    image, contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    thresh1=cv2.drawContours(thresh1, contours, 0,255,-1)
    thresh1=cv2.drawContours(thresh1, contours, 2,255,-1)
    '''
    thresh1=np.uint8(thresh1/255)
    z=im*thresh1[:,:,None]
    cv2.imwrite('koma1.jpg',z)

    
    
#操作1对手机截图，保存成sdcard/autojump.png
#操作2将sdcard/autojump.png保存到电脑桌面，和操作2_1效果一样，注意2_1有个小数点表示当前路径
def pull_screenshot():
    os.system('adb shell screencap -p /sdcard/autojump.png')            #1
    os.system('adb pull /sdcard/autojump.png {}'.format(os.getcwd()))            #2
    img1=cv2.imread('autojump.png')
    img1[1210:1280]=img1[130:200]                       #把分数部分移动到最下面
    img1=img1[300:1280,0:720]                           #截取部分图即可
    cv2.imwrite('autojump.png',img1)



#a,b分别是棋子到目标的横纵坐标的差值，z是长度，c是常数，将距离转换成时间
#x用来随机改变跳跃时间，发现无效后暂时不改
def sq(a,b,c=2.05):
    d=math.sqrt(a*a+b*b)
    z=d*c
    x=1
    #x=round((random.random()-0.5)/5+1,4)
    z=round(z*x)
    return z,x



#使用模板匹配获取棋子的中点，返回中点，和左上右下的坐标
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



#获取目标块的中点，顶点优先使用顶点下方两个像素位置的平均坐标，两侧优先使用左右顶点内侧2像素的平均坐标，
#然后取里中点更近的坐标，之后取顶点的横坐标和左/右点的纵坐标拼接即得到中点坐标。
#返回次坐标和canny获得的轮廓的上半部分
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
    #print(up1,left1,right1)
    
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

    cv2.circle(img,(up[1],up[0]),4,(0,0,255),-1)
    cv2.circle(img,(left[1],left[0]),4,(0,0,255),-1)
    cv2.circle(img,(right[1],right[0]),4,(0,0,255),-1)

    xx=up[1]
    a=abs(int(up[0]-left[0]))
    b=abs(int(up[0]-right[0]))
    yy=up[0]+min(a,b)
    
    cv2.circle(img,(xx,yy),4,(255,0,255),-1)
    return xx,yy,e



#循环匹配两种音符，找到就替换成背景，阈值取了0.7，感觉还可以
def delonpu(img,img0,onpu):
    while 1:
        w, h = onpu.shape[::-1]                             #获取元组列表反向元素的最便捷方法
        res = cv2.matchTemplate(img0,onpu,cv2.TM_CCOEFF_NORMED)                  
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val>0.7:
            print('出现音符，当前max_val=',max_val)
            img[max_loc[1]:max_loc[1]+h,max_loc[0]:max_loc[0]+w]=img[max_loc[1]:max_loc[1]+h,0:w]
            img0[max_loc[1]:max_loc[1]+h,max_loc[0]:max_loc[0]+w]=img0[max_loc[1]:max_loc[1]+h,0:w]
        else:
            return

        
def updown(x1=None,x2=None,t_=None):                        #跳跃
    if not x1:
        x1=random.randrange(100,600)
    if not x2:
        x2=random.randrange(800,1200)
    x3=random.randrange(-5,5)+x1
    x4=random.randrange(-5,5)+x2
    #x1=x2=x3=x4=111
    if not t_:
        t_=random.randint(4,7)
    
    s= 'adb shell input swipe {} {} {} {} {}'.format(x1,x2,x3,x4,t_)
    print(s)
    os.system(s)
        
        
        
#进行跳跃和记录的主函数   
def main(qq):
    step=0                            
    temp1=np.zeros((980, 720, 3))
    temp2=np.zeros((to, 720, 3))
    temp3=np.zeros((980-to, 720, 3))
    
    #下一行是获取当前时间的正规格式的非常好的方法
    name='{}.jpg'.format(time.strftime('%m-%d-%H-%M-%S',time.localtime(time.time())))
    while True:
        pull_screenshot()                       #截图并保存
        time.sleep(1)
        img=cv2.imread('autojump.png')          #读取截图
        
        #下面两种得到灰度图的方法，得到的图像信息居然不一样，上面这个信息更多
        img0=cv2.imread('autojump.png',0)           
        #img0=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                
        sco=score(img0)                                             #获取分数
        
        delonpu(img,img0,onpu)                      #替换音符1
        delonpu(img,img0,onpu1)                     #替换音符2
        w1,w2,w3=img.shape
     
        #将多个图片拼接成一张，方便核对节省空间，四张图片分别是跳前带标识图，跳后图，canny图切片，替换后灰度图。
        #这一部要在游戏失败前进行，否则无法保存失败的有效信息
        bigpic=np.zeros((w1,w2*3+3,w3))             
        bigpic[:,:w2,:]=temp1
        bigpic[:,3+w2:3+w2*2,:]=img
        bigpic[:to,3+w2*2:,:]=temp2
        bigpic[to:,3+w2*2:,:]=temp3
        cv2.imwrite(name,bigpic)

        #用模板匹配判断游戏是否失败
        res = cv2.matchTemplate(img0,aga,cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val>.9:
            print('游戏失败，即将重新开始')
            return 0,1
        mx,my,top_left,bottom_right=get_chess(img,img0)
        d1,d2=top_left
        d3,d4=bottom_right
 #mark>>>
        #音符可能匹配失败，所以将棋子周围替换成背景色。上方50px明显不够，左右20px也有风险，待修改
        d2,d3,d4=d2-50,d3+20,d4+20                             
        if d1>20:            
            d1=d1-20        
        else:                
            d1=0       
        img0[d2:d4,d1:d3]=img0[d2:d4,1].reshape((d4-d2,-1))
 #mark<<<      
    
        nx,ny,dst=get_pic(img,img0)
        #将灰度图转成rgb图，才能被上面的代码合成一张图。
        #dst1和dst2会被保存成临时变量，在跳跃并截图后，供下次合成图片使用。
        dst1=np.repeat(dst.ravel(),3).reshape((to,720,3))                   
        dst2=np.repeat(img0[:980-to,:].ravel(),3).reshape((980-to,720,3))
     
        z,x=sq(mx-nx,my-ny)
        
        updown(t_=z)
        step+=1
        print('目标{}当前{}  ||'.format(qq,sco),
              '{},{}==>{},{}  ||x={},z={},step={}'.format(mx,my,nx,ny,x,z,step))
        time.sleep(3)       #2.5秒肯定不够
        
        temp1=img
        cv2.putText(dst1,r'{},{}/{},{}/{}'.format(mx,my,nx,ny,z),
                    (0,50), cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2,cv2.LINE_AA)
        temp2=dst1
        temp3=dst2
        
        a=random.randrange(1,9)
        if a==1:                                    #模拟暂时休息，似乎不要还没用
            print('*'*11,'休息9秒')
            #time.sleep(9)
            
        if sco>qq:                              #从图片识别当前分数，超过目标分数时自杀
            updown(t_=1211)
            time.sleep(3)
            
            pull_screenshot()
            img0=cv2.imread('autojump.png',0)
            res = cv2.matchTemplate(img0,ky,cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            cv2.imwrite(name,img0)
            if max_val>0.95:                        #判定没作弊才增加目标分数
                print('>'*55,'作弊认定，目标不变')
                os.remove(name)
                return 0,1
            print('='*55,'成功，目标增加')
            return 0,0


x=0                                         #流程判断的初始值
qq=200                                      #目标分数
onpu =cv2.imread('konpu.jpg',0)             #这里依次是音符1，音符2，再玩一次，可疑操作的截图
onpu1 =cv2.imread('konpu1.jpg',0)
aga=cv2.imread('kagain.jpg',0)
ky=cv2.imread('ky.jpg',0)

while 1:
    print('x=',x,'qq=',qq)
    if x==0:
        time.sleep(3)
        x=1
        updown(x1=500,x2=1050)
    time.sleep(2)
    if x==1:
        x,y=main(qq)
        
        if y==0:
            qq+=50


