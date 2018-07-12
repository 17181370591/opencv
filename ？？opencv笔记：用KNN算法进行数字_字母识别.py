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


==========================================================================================

'''
英文字母的 OCR
　　接下来我们来做英文字母的 OCR。和上面做法一样，但是数据和特征集有一些不同。
  现在 OpenCV 给出的不是图片了，而是一个数据文件（/samples/cpp/letter-recognition.data）。
  如果打开它的话，你会发现它有 20000 行，第一样看上去就像是垃圾。实际上每一行的第一列是我们的一个字母标记。
  接下来的 16 个数字是它的不同特征。这些特征来源于UCI Machine LearningRepository。
有 20000 个样本可以使用，我们取前 10000 个作为训练样本，剩下的10000 个作为测试样本。
我们应在先把字母表转换成 asc 码，因为我们不正直接处理字母。
'''

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the data, converters convert the letter to a number。读取字母数据
data= np.loadtxt('letter-recognition.data', dtype= 'float32', delimiter = ',',
                    converters= {0: lambda ch: ord(ch)-ord('A')})

# split the data to two, 10000 each for train and test
train, test = np.vsplit(data,2)               #竖直平分，前半训练后半测试

# split trainData and testData to features and responses
responses, trainData = np.hsplit(train,[1])       #第一列是结果，后面列是特征值
labels, testData = np.hsplit(test,[1])

# Initiate the kNN, classify, measure accuracy.
knn = cv2.ml.KNearest_create()
knn.train(trainData, cv2.ml.ROW_SAMPLE, responses)
ret, result, neighbours, dist = knn.findNearest(testData, k=5)

correct = np.count_nonzero(result == labels)
accuracy = correct*100.0/10000
print (accuracy)
