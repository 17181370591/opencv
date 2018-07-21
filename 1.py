import matplotlib.pyplot as plt,cv2,numpy as np,pytesseract,PIL

p=r'C:\Users\Administrator\Desktop\111\autoj.png'
a=cv2.imread(p,0)[130:200,:]
r= pytesseract.image_to_string(a,lang='all',config='-psm 7')
print(r)

'''
box文件里8 244 1 266 30 0，表示数字8，左右坐标244,266，所以宽度22；
上下坐标-30,-1（距离底部的高度），高度29，最后好像必须是0
tesseract all.tif all nobatch box.train
unicharset_extractor all.box
mftraining -F font_properties -U unicharset all.tr
cntraining all.tr
all.
#shapetable,normproto,pffmtable,inttemp ,
combine_tessdata all
'''
