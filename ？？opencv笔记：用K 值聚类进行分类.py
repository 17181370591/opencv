'''
OpenCV 中的 K 值聚类
目标
　　• 学习使用 OpenCV 中的函数 cv2.kmeans() 对数据进行分类


48.2.1 理解函数的参数
输入参数
理解函数的参数
输入参数
　　1. samples: 应该是 np.float32 类型的数据，每个特征应该放在一列。
　　2. nclusters(K): 聚类的最终数目。
　　3. criteria: 终止迭代的条件。当条件满足时，算法的迭代终止。它应该是一个含有 3 个成员的元组，
  它们是（typw，max_iter，epsilon）：
　　　　• type 终止的类型：有如下三种选择：
　　　　　　– cv2.TERM_CRITERIA_EPS 只有精确度 epsilon 满足是停止迭代。
　　　　　　– cv2.TERM_CRITERIA_MAX_ITER 当迭代次数超过阈值时停止迭代。
　　　　　　– cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER上面的任何一个条件满足时停止迭代。
　　　　• max_iter 表示最大迭代次数。
　　　　• epsilon 精确度阈值。
　　4. attempts: 使用不同的起始标记来执行算法的次数。算法会返回紧密度最好的标记。紧密度也会作为输出被返回。
　　5. flags：用来设置如何选择起始重心。通常我们有两个选择:cv2.KMEANS_PP_CENTERS和cv2.KMEANS_RANDOM_CENTERS。
输出参数
　　1. compactness：紧密度，返回每个点到相应重心的距离的平方和。
　　2. labels：标志数组（与上一节提到的代码相同），每个成员被标记为 0，1等
　　3. centers：由聚类的中心组成的数组。
现在我们用 3 个例子来演示如何使用 K 值聚类。

48.2.2 仅有一个特征的数据
　　假设我们有一组数据，每个数据只有一个特征（1 维）。例如前面的 T 恤问题，我们只使用人们的身高来决定 T 恤的大小。
我们先来产生一些随机数据，并使用 Matplotlib 将它们绘制出来。

现在我们有一个长度为 50，取值范围为 0 到 255 的向量 z。我已经将向量 z 进行了重排，将它变成了一个列向量。
当每个数据含有多个特征是这会很有用。然后我们数据类型转换成 np.float32。
我们得到下图：

现在我们使用 KMeans 函数。在这之前我们应该首先设置好终止条件。我的终止条件是：
算法执行 10 次迭代或者精确度 epsilon = 1.0。

返回值有紧密度（compactness）, 标志和中心。在本例中我的到的中心是 60 和 207。
标志的数目与测试数据的多少是相同的，每个数据都会被标记上“0”，“1”等。这取决与它们的中心是什么。
现在我们可以根据它们的标志将把数据分两组。

现在将 A 组数用红色表示，将 B 组数据用蓝色表示，重心用黄色表示。


'''
import numpy as np
import cv2
from matplotlib import pyplot as plt

x = np.random.randint(25,100,25)
y = np.random.randint(175,255,25)
z = np.hstack((x,y))
z = z.reshape((50,1))
z = np.float32(z)
plt.hist(z,256,[0,256])                       #生成随机数据，拼接，画图

# Define criteria = ( type, max_iter = 10 , epsilon = 1.0 )
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)        #设置聚类参数


# Set flags (Just to avoid line break in the code)
flags = cv2.KMEANS_RANDOM_CENTERS                                       #设置随机的初始重心？

# Apply KMeans
#labels和z的shape一样，每个值是z的值对应的标签。centers是不同标签的重心
compactness,labels,centers = cv2.kmeans(z,2,None,criteria,10,flags)

A = z[labels==0]
B = z[labels==1]                                                      #按标签获取数据

plt.hist(A,256,[0,256],color = 'r')
plt.hist(B,256,[0,256],color = 'b')
plt.hist(centers,64,[0,256],color = 'y')
plt.show()
