import matplotlib.pyplot as plt,cv2,numpy as np,pytesseract,PIL

a=cv2.imread('小票.jpg',1)

b=cv2.imread('小票.jpg',0)
ret, b = cv2.threshold(b,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

kernel = np.ones((1,15),np.uint8)        
#b= cv2.dilate(b,kernel,iterations = 1)
o=5
#kernel = np.ones((o,o),np.uint8)
b=cv2.morphologyEx(b, cv2.MORPH_CLOSE, kernel)

i,contours,h= cv2.findContours(b,0,cv2.CHAIN_APPROX_NONE)
#img= cv2.drawContours(a, contours, -1, (0,255,0),2)
for cnt in contours:
    x,y,w,h = cv2.boundingRect(cnt)
    a = cv2.rectangle(a,(x,y),(x+w,y+h),(0,255,0),2)

cv2.imshow('',a)
