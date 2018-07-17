#https://www.cnblogs.com/mikewolf2002/p/3330390.html

import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('y5.jpg')
mask = np.zeros(img.shape[:2],np.uint8)

bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)
rect = (70,40,355,480)
# 函数的返回值是更新的 mask, bgdModel, fgdModel
cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
#img = img*mask2[:,:,np.newaxis]
#plt.imshow(img),plt.colorbar(),plt.show()
#cv2.imshow('',img)


#mask[390:410,390:410]=1
mask[450:470,130:150]=0
mask, bgdModel, fgdModel = cv2.grabCut(img,mask,None,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_MASK)
mask = np.where((mask==2)|(mask==0),0,1).astype('uint8')
img = img*mask[:,:,np.newaxis]
cv2.imshow('',img)

'''
img = cv2.imread('y5.jpg')
mask = np.ones(img.shape[:2],np.uint8)
mask=mask*3
mask[0:100,300:500]=0
mask[0:260,0:60]=0
mask[140:390,140:280]=1
mask[150:240,400:490]=1

bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)
mask, bgdModel, fgdModel = cv2.grabCut(img,mask,None,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_MASK)

mask = np.where((mask==2)|(mask==0),0,1).astype('uint8')
img = img*mask[:,:,np.newaxis]
cv2.imshow('',img)


'''
