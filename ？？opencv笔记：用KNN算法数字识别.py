'''
使用 kNN 对手写数字 OCR

目标
　　• 要根据我们掌握的 kNN 知识创建一个基本的 OCR 程序
　　• 使用 OpenCV 自带的手写数字和字母数据测试我们的程序
46.2.1 手写数字的 OCR
　　我们的目的是创建一个可以对手写数字进行识别的程序。为了达到这个目的我们需要训练数据和测试数据。
  OpenCV 安装包中有一副图片（/samples/python2/data/digits.png）, 其中有 5000 个手写数字（每个数字重复500遍）。
  每个数字是一个 20x20 的小图。所以第一步就是将这个图像分割成 5000个不同的数字。
  我们在将拆分后的每一个数字的图像重排成一行含有 400 个像素点的新图像。这个就是我们的特征集，所有像素的灰度值。
  这是我们能创建的最简单的特征集。我们使用每个数字的前 250 个样本做训练数据，剩余的250 个做测试数据。
  让我们先准备一下：
'''

import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('wz.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)    

# Now we split the image to 5000 cells, each 20x20 size
cells = [np.hsplit(row,100) for row in np.vsplit(gray,50)]         #先纵向切成50份，然后横向切成100份

# Make it into a Numpy array. It size will be (50,100,20,20)
x = np.array(cells)                                                 #cells是列表

# Now we prepare train_data and test_data.
train = x[:,:50].reshape(-1,400).astype(np.float32) # Size = (2500,400)
test = x[:,50:100].reshape(-1,400).astype(np.float32) # Size = (2500,400)

# Create labels for train and test data
k = np.arange(10)
train_labels = np.repeat(k,250)[:,np.newaxis]                       #注意repeat的用法
#train_labels = np.repeat(k,250).reshape(-1,1)
test_labels = train_labels.copy()

# Initiate kNN, train the data, then test it with test data for k=1
knn = cv2.ml.KNearest_create()                                      
knn.train(train, cv2.ml.ROW_SAMPLE,train_labels)
ret,result,neighbours,dist = knn.findNearest(test,k=5)

# Now we check the accuracy of classification
# For that, compare the result with test_labels and check which are wrong
matches = result==test_labels
correct = np.count_nonzero(matches)                                 #正确识别的数量
#correct =np.argwhere(matches==True).shape[0]
accuracy = correct*100.0/result.size
print (accuracy)
