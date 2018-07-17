'''
OpenCV  中的 Haar  级联检测
OpenCV 自带了训练器和检测器。如果你想自己训练一个分类器来检测
汽车，飞机等的话，可以使用 OpenCV 构建。其中的细节在这里：Cascade
Classifier Training
现在我们来学习一下如何使用检测器。OpenCV 已经包含了很多已经训练
好的分类器，其中包括：面部，眼睛，微笑等。这些 XML 文件保存在/opencv/
data/haarcascades/文件夹中。下面我们将使用 OpenCV 创建一个面部和眼
部检测器。
首先我们要加载需要的 XML 分类器。然后以灰度格式加载输入图像或者
是视频。
'''
import numpy as np
import cv2

pathf = r'E:\ocv\haarcascade_frontalface_default.xml'

pathe = r'E:\ocv\haarcascade_eye.xml'

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
face_cascade.load(pathf)
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
eye_cascade.load(pathe)
img = cv2.imread('r2.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray,
                scaleFactor = 1.3,
   minNeighbors = 5,minSize = (5,5))
for (x,y,w,h) in faces:
    img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(roi_gray)
    for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
cv2.imwrite('ren.jpg',img)
