import numpy as np
import cv2

#245,170,255,200
img = cv2.imread('y6.jpg')
img[170:200,245:255]=(0,255,255)
img[310:322,100:220]=(0,255,255)
cv2.imshow('img',img)
mask = np.zeros(img.shape[:2])
mask[170:200,245:255]=255
mask[310:322,100:220]=255
mask=np.uint8(mask)
dst = cv2.inpaint(img,mask,3,cv2.INPAINT_TELEA)
cv2.imshow('dst',dst)
