#http://www.cnblogs.com/Undo-self-blog/p/8424056.html

import cv2
import numpy as np

def nothing(x):
    pass
switch = '0 : OFF \n1 : ON'

# Create a black image, a window

cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('R','image',0,255,nothing)
cv2.createTrackbar('G','image',0,255,nothing)
cv2.createTrackbar('B','image',0,255,nothing)

# create switch for ON/OFF functionality

cv2.createTrackbar(switch, 'image',0,1,nothing)
img = np.zeros((300,512,3), np.uint8)
while(1):
    
    cv2.imshow('image',img)
    k = cv2.waitKey(1) 
    if k == 27:
        break

    # get current positions of four trackbars
    r = cv2.getTrackbarPos('R','image')
    g = cv2.getTrackbarPos('G','image')
    b = cv2.getTrackbarPos('B','image')
    s = cv2.getTrackbarPos(switch,'image')

    if s == 0:
        img[:] = 0
    else:
        img[:] = [b,g,r]

cv2.destroyAllWindows()
