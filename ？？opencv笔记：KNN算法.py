'''
K 近邻（k-Nearest Neighbour ）

46.1 理解 K 近邻
目标
　　• 本节我们要理解 k 近邻（kNN）的基本概念。
原理
　　kNN 可以说是最简单的监督学习分类器了。想法也很简单，就是找出测试数据在特征空间中的最近邻居。
  我们将使用下面的图片介绍它。

　　　　Understanding kNN
上图中的对象可以分成两组，蓝色方块和红色三角。每一组也可以称为一个 类。我们可以把所有的这些对象看成是一个城镇中房子，
而所有的房子分别属于蓝色和红色家族，而这个城镇就是所谓的特征空间。（你可以把一个特征空间看成是所有点的投影所在的空间。
例如在一个 2D 的坐标空间中，每个数据都两个特征 x 坐标和 y 坐标，你可以在 2D 坐标空间中表示这些数据。
如果每个数据都有 3 个特征呢，我们就需要一个 3D 空间。N 个特征就需要 N 维空间，这个 N 维空间就是特征空间。
在上图中，我们可以认为是具有两个特征色2D 空间）。
现在城镇中来了一个新人，他的新房子用绿色圆盘表示。我们要根据他房子的位置把他归为蓝色家族或红色家族。
我们把这过程成为 分类。我们应该怎么做呢？因为我们正在学习看 kNN，那我们就使用一下这个算法吧。
一个方法就是查看他最近的邻居属于那个家族，从图像中我们知道最近的是红色三角家族。所以他被分到红色家族。
这种方法被称为简单 近邻，因为分类仅仅决定与它最近的邻居。
但是这里还有一个问题。红色三角可能是最近的，但如果他周围还有很多蓝色方块怎么办呢？
此时蓝色方块对局部的影响应该大于红色三角。所以仅仅检测最近的一个邻居是不足的。所以我们检测 k 个最近邻居。
谁在这 k 个邻居中占据多数，那新的成员就属于谁那一类。如果 k 等于 3，也就是在上面图像中检测 3 个最近的邻居。
他有两个红的和一个蓝的邻居，所以他还是属于红色家族。但是如果 k 等于 7 呢？他有 5 个蓝色和 2 个红色邻居，
现在他就会被分到蓝色家族了。k 的取值对结果影响非常大。更有趣的是，如果 k 等于 4呢？两个红两个蓝。这是一个死结。
所以 k 的取值最好为奇数。这中根据 k 个最近邻居进行分类的方法被称为 kNN。
在 kNN 中我们考虑了 k 个最近邻居，但是我们给了这些邻居相等的权重，这样做公平吗？以 k 等于 4 为例，
我们说她是一个死结。但是两个红色三角比两个蓝色方块距离新成员更近一些。所以他更应该被分为红色家族。
那用数学应该如何表示呢？我们要根据每个房子与新房子的距离对每个房子赋予不同的权重。
距离近的具有更高的权重，距离远的权重更低。然后我们根据两个家族的权重和来判断新房子的归属，谁的权重大就属于谁。
这被称为 修改过的kNN。那这里面些是重要的呢？
• 我们需要整个城镇中每个房子的信息。因为我们要测量新来者到所有现存房子的距离，并在其中找到最近的。
如果那里有很多房子，就要占用很大的内存和更多的计算时间。
• 训练和处理几乎不需要时间。
现在我们看看 OpenCV 中的 kNN。

46.1.1 OpenCV 中的 kNN
　　我们这里来举一个简单的例子，和上面一样有两个类。下一节我们会有一个更好的例子。
这里我们将红色家族标记为 Class-0，蓝色家族标记为 Class-1。还要再创建 25 个训练数据，
把它们非别标记为 Class-0 或者 Class-1。Numpy中随机数产生器可以帮助我们完成这个任务。
然后借助 Matplotlib 将这些点绘制出来。红色家族显示为红色三角蓝色家族显示为蓝色方块。
'''


import cv2
import numpy as np
import matplotlib.pyplot as plt

# Feature set containing (x,y) values of 25 known/training data
trainData = np.random.randint(0,100,(25,2)).astype(np.float32)
print(trainData)
# Labels each one either Red or Blue with numbers 0 and 1
responses = np.random.randint(0,2,(25,1)).astype(np.float32)
print('responses=',responses)
# Take Red families and plot them
red = trainData[responses.ravel()==0]
plt.scatter(red[:,0],red[:,1],80,'r','^')

# Take Blue families and plot them
blue = trainData[responses.ravel()==1]
plt.scatter(blue[:,0],blue[:,1],80,'b','s')


#下面是要验证的数据，可以是一个点，也可以是点集
#newcomer = np.random.randint(0,100,(1,2)).astype(np.float32)
newcomer = np.random.randint(0,100,(10,2)).astype(np.float32)
plt.scatter(newcomer[:,0],newcomer[:,1],80,'g','o')


'''
下面就是 kNN 算法分类器的初始化，我们要传入一个训练数据集，以及与训练数据对应的分类来训练 kNN 分类器（构建搜索树）。
最后要使用 OpenCV 中的 kNN 分类器，我们给它一个测试数据，让它来进行分类。在使用 kNN 之前，
我们应该对测试数据有所了解。我们的数据应该是大小为数据数目乘以特征数目的浮点性数组。
然后我们就可以通过计算找到测试数据最近的邻居了。我们可以设置返回的最近邻居的数目。返回值包括：
　　1. 由 kNN 算法计算得到的测试数据的类别标志（0 或 1）。如果你想使用最近邻算法，只需要将 k 设置为 1，
      k 就是最近邻的数目。
　　2. k 个最近邻居的类别标志。
　　3. 每个最近邻居到测试数据的距离。
让我们看看它是如何工作的。测试数据被标记为绿色。
'''

knn = cv2.ml.KNearest_create()
knn.train(trainData, cv2.ml.ROW_SAMPLE,responses)
ret, results, neighbours ,dist = knn.findNearest(newcomer, 3)

print ("result: ", results,"\n")
print ("neighbours: ", neighbours,"\n")
print ("distance: ", dist)

plt.show()
