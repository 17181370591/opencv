#http://www.cnblogs.com/Undo-self-blog/p/8436480.html
#思路是制作两幅图的高斯金字塔，然后用图a减去图a压缩再放大后的图制作拉普拉斯金字塔，
#然后把两个拉普拉斯金字塔缝合，再对新金字塔进行从小开始放大并与下一个元素求和

'''
目标
　　• 学习图像金字塔
　　• 使用图像创建一个新水果：“橘子苹果”
　　• 将要学习的函数有：cv2.pyrUp()，cv2.pyrDown()。
20.1 原理
　　一般情况下，我们要处理是一副具有固定分辨率的图像。但是有些情况下，
  我们需要对同一图像的不同分辨率的子图像进行处理。比如，我们要在一幅图像中查找某个目标，比如脸，
  我们不知道目标在图像中的尺寸大小。这种情况下，我们需要创建创建一组图像，这些图像是具有不同分辨率的原始图像。
  我们把这组图像叫做图像金字塔（简单来说就是同一图像的不同分辨率的子图集合）。
  如果我们把最大的图像放在底部，最小的放在顶部，看起来像一座金字塔，故而得名图像金字塔。
　　有两类图像金字塔：高斯金字塔和拉普拉斯金字塔。
　　高斯金字塔的顶部是通过将底部图像中的连续的行和列去除得到的。
  顶部图像中的每个像素值等于下一层图像中 5 个像素的高斯加权平均值。
  这样操作一次一个 MxN 的图像就变成了一个 M/2xN/2 的图像。所以这幅图像的面积就变为原来图像面积的四分之一。
  这被称为 Octave。连续进行这样的操作我们就会得到一个分辨率不断下降的图像金字塔。
  我们可以使用函数cv2.pyrDown() 和 cv2.pyrUp() 构建图像金字塔。
　　函数 cv2.pyrDown() 从一个高分辨率大尺寸的图像向上构建一个金子塔（尺寸变小，分辨率降低）。
  拉普拉金字塔的图像看起来就像边界图，其中很多像素都是 0。他们经常被用在图像压缩中。
  拉普拉斯金字塔可以有高斯金字塔计算得来，公式如下：L i = G i − PyrUp(G i+1 )
'''



'''
使用金字塔进行图像融合
　　图像金字塔的一个应用是图像融合。例如，在图像缝合中，你需要将两幅图叠在一起，
  但是由于连接区域图像像素的不连续性，整幅图的效果看起来会很差。这时图像金字塔就可以排上用场了，
  他可以帮你实现无缝连接。这里的一个经典案例就是将两个水果融合成一个，看看下图也许你就明白我在讲什么了。
 
你可以通过阅读后边的更多资源来了解更多关于图像融合，拉普拉斯金字塔的细节。
实现上述效果的步骤如下：
　　1. 读入两幅图像，苹果和句子
　　2. 构建苹果和橘子的高斯金字塔（6 层）
　　3. 根据高斯金字塔计算拉普拉斯金字塔
　　4. 在拉普拉斯的每一层进行图像融合（苹果的左边与橘子的右边融合）
　　5. 根据融合后的图像金字塔重建原始图像。
下图是摘自《学习 OpenCV》展示了金子塔的构建，以及如何从金字塔重建原始图像的过程。
整个过程的代码如下。（为了简单，每一步都是独立完成的，这回消耗更多、的内存，如果你愿意的话可以对他进行优化）
'''



import cv2,os
import numpy as np,sys

nu=0                            #保存图像时用来起名，跟主程序无关
mm=6                            #设置放大缩小的次数

p=os.getcwd()+'\\1\\{}.jpg'
A = cv2.imread('3.jpg')
B = cv2.imread('q2.jpg')                    #AB两个图需要size相同
print(p.format(nu),A.shape,B.shape)
# generate Gaussian pyramid for A



G = A.copy()                        #获取down金字塔
gpA = [G]
for i in range(mm):                 #连续mm次长宽减半，四舍五入
    G = cv2.pyrDown(G)
    gpA.append(G)
    #print(G.shape,'11')
    cv2.imwrite(p.format(nu),G)
    nu+=1

    
    
# generate Gaussian pyramid for B
G = B.copy()                        #连续mm次长宽加倍，获取up金字塔
gpB = [G]
for i in range(mm):
    G = cv2.pyrDown(G)
    gpB.append(G)
    #print(G.shape,'22')
    cv2.imwrite(p.format(nu),G)
    nu+=1

    
    
# generate Laplacian Pyramid for A
##获取Laplacian金字塔，方法是用图a减去a减半在加倍的图，生成的图类似于边界图
lpA = [gpA[mm-1]]                               
for i in range(mm-1,0,-1):
    GE = cv2.pyrUp(gpA[i])
    #print(gpA[i-1].shape,GE.shape)
    x,y,z=gpA[i-1].shape
    L = cv2.subtract(gpA[i-1],GE[:x,:y,:z])                 
    #两个大小一样的图，减半后大小依旧相同，但是加倍后可能出现不同，所以使用切片使他们尺寸相同
    #这里更通用的写法是x，y取两个图的最小值，然后同时对两个图切片
    
    lpA.append(L)
    #print(L.shape,'33')
    cv2.imwrite(p.format(nu),L)
    nu+=1

    
    
# generate Laplacian Pyramid for B，同上
lpB = [gpB[mm-1]]
for i in range(mm-1,0,-1):
    GE = cv2.pyrUp(gpB[i])
    x,y,z=gpA[i-1].shape
    L = cv2.subtract(gpB[i-1],GE[:x,:y,:z])
    lpB.append(L)
    #print(L.shape,'44')
    cv2.imwrite(p.format(nu),L)
    nu+=1

    
    
    
# Now add left and right halves of images in each level
#对两个Laplacian金字塔的每幅图各取一半，进行缝合，索引一定要是整数，生成缝合后的金字塔
LS = []                             
for la,lb in zip(lpA,lpB):
    rows,cols,dpt = la.shape
    print(la.shape,lb.shape)
    he=int(cols/2)
    ls = np.hstack((la[:,0:he], lb[:,he:]))
    LS.append(ls)
    cv2.imwrite(p.format(nu),ls)
    nu+=1

    
    
    
# now reconstruct
#对缝合后的金字塔求和，获取最终图片
ls_ = LS[0]
for i in range(1,mm):
    ls_ = cv2.pyrUp(ls_)
    #print(ls_.shape,LS[i].shape)
    x,y,z=LS[i].shape
    ls_ = cv2.add(ls_[:x,:y,:z], LS[i])
    cv2.imwrite(p.format(nu),ls_)
    nu+=1

    
    
# image with direct connecting each half
#直接取半缝合，用来对比效果
he=int(cols/2)
real = np.hstack((A[:,:he],B[:,he:]))


cv2.imwrite('1/Pyramid_blending2.jpg',ls_)
cv2.imwrite('1/Direct_blending.jpg',real)
