import cv2
import numpy as np

img=cv2.imread('1.jpg')
px=img[100,100]
print(px)
blue=img[100,100,0]
print(blue)

Numpy 是经过优化了的进行快速矩阵运算的软件包。所以我们不推荐逐个获取像素值并修改，这样会很慢，能有矩阵运算就不要用循环。
注意：上面提到的方法被用来选取矩阵的一个区域，比如说前 5 行的后 3列。对于获取每一个像素值，也许使用 Numpy 的 array.item() 和 array.itemset() 会更好。但是返回值是标量。如果你想获得所有 B，G，R 的
值，你需要使用 array.item() 分割他们。

获取像素值及修改的更好方法:

print(img.item(10,10,2))
print(img.item(123))
for i in range(1,111):
    for j in range(1,111):
        img.itemset((i,j,0),220)
        img.itemset((i,j,1),220)
        img.itemset((i,j,2),220)

cv2.imshow('',img)

注意：在debug时 img.dtype 非常重要。因为在 OpenCV Python 代码中经常出现数据类型的不一致。


#拷贝到图像
img=cv2.imread('2.jpg')
ball=img[185:270,46:190]

img[140:225,746:890]=ball
img=cv2.imshow('test', img)


#切割合并图像，有两种切割方法，split和numpy索引，后者更快更好
b,g,r=cv2.split(img)
b1=img[:,:,0]
print(np.argwhere(b1!=b))
img1=cv2.merge((img[:,:,0],img[:,:,1],img[:,:,2]))
cv2.imshow('1',img1)
cv2.waitKey(0)              #等待键盘输入，按下任何键都会继续执行
cv2.destroyAllWindows()


为图像扩边（填充）
　　如果你想在图像周围创建一个边，就像相框一样，你可以使用 cv2.copyMakeBorder()函数。这经常在卷积运算或 0 填充时被用到。这个函数包括如下参数：
　　• src 输入图像
　　• top, bottom, left, right 对应边界的像素数目。
　　• borderType 要添加那种类型的边界，类型如下：
　　　　– cv2.BORDER_CONSTANT 添加有颜色的常数值边界，还需要下一个参数（value）。
　　　　– cv2.BORDER_REFLECT 边界元素的镜像。比如: fedcba|abcde-fgh|hgfedcb
　　　　– cv2.BORDER_REFLECT_101 or cv2.BORDER_DEFAULT跟上面一样，但稍作改动。例如: gfedcb|abcdefgh|gfedcba
　　　　– cv2.BORDER_REPLICATE 重复最后一个元素。例如: aaaaaa|abcdefgh|hhhhhhh
　　　　– cv2.BORDER_WRAP 不知道怎么说了, 就像这样: cdefgh|abcdefgh|abcdefg
　　• value 边界颜色，如果边界的类型是 cv2.BORDER_CONSTANT

为了更好的理解这几种类型请看下面的演示程序。
BLUE=[0,0,255]
img1=cv2.imread('o.jpg')
replicate = cv2.copyMakeBorder(img1,10,10,10,10,cv2.BORDER_REPLICATE)
reflect = cv2.copyMakeBorder(img1,10,10,10,10,cv2.BORDER_REFLECT)
reflect101 = cv2.copyMakeBorder(img1,10,10,10,10,cv2.BORDER_REFLECT_101)
wrap = cv2.copyMakeBorder(img1,10,10,10,10,cv2.BORDER_WRAP)
constant= cv2.copyMakeBorder(img1,10,20,30,40,cv2.BORDER_CONSTANT,value=BLUE)
plt.subplot(231),plt.imshow(img1,'gray'),plt.title('ORIGINAL')
plt.subplot(232),plt.imshow(replicate,'gray'),plt.title('REPLICATE')
plt.subplot(233),plt.imshow(reflect,'gray'),plt.title('REFLECT')
plt.subplot(234),plt.imshow(reflect101,'gray'),plt.title('REFLECT_101')
plt.subplot(235),plt.imshow(wrap,'gray'),plt.title('WRAP')
plt.subplot(236),plt.imshow(constant,'gray'),plt.title('CONSTANT')
plt.show()


图像加法
　　你可以使用函数 cv2.add() 将两幅图像进行加法运算，当然也可以直接使用 numpy，res=img1+img。两幅图像的大小，类型必须一致，或者第二个图像可以使一个简单的标量值。
注意：OpenCV 中的加法与 Numpy 的加法是有所不同的。OpenCV 的加法是一种饱和操作，而 Numpy 的加法是一种模操作。
例如下面的两个例子：

x = np.uint8([250])
y = np.uint8([10])
print cv2.add(x,y) # 250+10 = 260 => 255
[[255]]
print x+y # 250+10 = 260 % 256 = 4
[4]
这种差别在你对两幅图像进行加法时会更加明显。OpenCV 的结果会更好一点。所以我们尽量使用 OpenCV 中的函数。



 图像混合
　　这其实也是加法，但是不同的是两幅图像的权重不同，这就会给人一种混合或者透明的感觉。
要求两幅图的尺寸一样，还有没有其他要求未测试
这里dst=cv2.add(o*0.5,o1*0.8)，超过255会饱和
合理使用饱和可以制作好看的镂空效果
o = cv2.imread('o.jpg')         #logo
o1 = cv2.imread('o1.jpg')       #chino


dst = cv2.addWeighted(o,.5,o1,.8,0)
d1=(100,330)
d2=(320,50)
d3=(440,350)

print(o[d1],o1[d1],dst[d1])
print(o[d2],o1[d2],dst[d2])
print(o[d3],o1[d3],dst[d3])
cv2.imshow('dst',dst)
dst = cv2.addWeighted(o,1,o1,1,0)
cv2.imshow('dst',dst)



#使用加权图像混合制作fade-toggle效果
#使用切片制作图片滚动效果
#需要特别注意：在循环里imshow无法打开图片，需要在后面添加延迟，例如cv2.waitKey(30)
o = cv2.imread('o.jpg')         #logo
o1 = cv2.imread('o1.jpg')       #chino
cv2.namedWindow('dst')
dst=o
a,b=0,1
c=.01
def f():
    global a,b,c
    dst = cv2.addWeighted(o,a,o1,b,0)
    a+=c
    b-=c
    print(a,b,c)
    return dst
def g():
    global a,b,c
    x=int(500-a*500)
    dst[:,x:]=o1[:,x:]
    a+=c
    return dst
while a<1:        
    dst=g()
    cv2.imshow('dst',dst) 
    cv2.waitKey(int(c*1000)) 


    
按位运算
这里包括的按位操作有：AND，OR，NOT，XOR 等。当我们提取图像的一部分，选择非矩形 ROI 时这些操作会很有用（下一章你就会明白）。下面的例子就是教给我们如何改变一幅图的特定区域。我想把 OpenCV 的标志放到另一幅图像上。如果我使用加法，颜色会改变，如果使用混合，会得到透明效果，但是我不想要透明。如果他是矩形我可以象上一章那样使用 ROI。但是他不是矩形。但是我们可以通过下面的按位运算实现：
img1 = cv2.imread('o1.jpg')
img2 = cv2.imread('o.jpg')

rows,cols,channels = img2.shape
roi = img1[0:rows, 0:cols ]

img2gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)

ret, mask = cv2.threshold(img2gray, 76,255, cv2.THRESH_BINARY)
mask_inv = cv2.bitwise_not(mask)

img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)

img2_fg = cv2.bitwise_and(img2,img2,mask = mask)

dst = cv2.add(img1_bg,img2_fg)
img1[0:rows, 0:cols ] = dst
cv2.imshow('res',img1)



