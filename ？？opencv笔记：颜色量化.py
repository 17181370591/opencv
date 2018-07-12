'''
颜色量化
　　颜色量化就是减少图片中颜色数目的一个过程。为什么要减少图片中的颜色呢？减少内存消耗！
  有些设备的资源有限，只能显示很少的颜色。在这种情况下就需要进行颜色量化。我们使用 K 值聚类的方法来进行颜色量化。
  没有什么新的知识需要介绍了。现在有 3 个特征：R，G，B。
  所以我们需要把图片数据变形成 Mx3（M 是图片中像素点的数目）的向量。
  聚类完成后，我们用聚类中心值替换与其同组的像素值，这样结果图片就只含有指定数目的颜色了。下面是代码：
  
'''
'''
理解函数的参数
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
　　5. flags：用来设置如何选择起始重心。通常我们有两个选择：
          cv2.KMEANS_PP_CENTERS和 cv2.KMEANS_RANDOM_CENTERS。
输出参数
　　1. compactness：紧密度，返回每个点到相应重心的距离的平方和。
　　2. labels：标志数组（与上一节提到的代码相同），每个成员被标记为 0，1等
　　3. centers：由聚类的中心组成的数组。
  '''

import numpy as np
import cv2

img = cv2.imread('2.jpg')
Z = img.reshape((-1,3))

# convert to np.float32
Z = np.float32(Z)

# define criteria, number of clusters(K) and apply kmeans()
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 3
ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

# Now convert back into uint8, and make original image
center = np.uint8(center)
res = center[label.flatten()]
res2 = res.reshape(img.shape)

cv2.imshow('res2',res2)

