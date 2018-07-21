import cv2,numpy as np,pytesseract


p=r'C:\Users\Administrator\Desktop\111\autoj.png'
a=cv2.imread(p,0)[130:200,:]

'''
Usage:tesseract imagename outputbase [-l lang] [-psm pagesegmode] [configfile...]
pagesegmode values are:
0 = Orientation and script detection (OSD) only.
1 = Automatic page segmentation with OSD.
2 = Automatic page segmentation, but no OSD, or OCR
3 = Fully automatic page segmentation, but no OSD. (Default)
4 = Assume a single column of text of variable sizes.
5 = Assume a single uniform block of vertically aligned text.
6 = Assume a single uniform block of text.
7 = Treat the image as a single text line.
8 = Treat the image as a single word.
9 = Treat the image as a single word in a circle.
10 = Treat the image as a single character.
-l lang and/or -psm pagesegmode must occur before anyconfigfile.
'''
#用all.traineddata对图片数组a进行单行识别
r= pytesseract.image_to_string(a,lang='all',config='-psm 7')
print(r)




'''
一些traneddata：https://github.com/tesseract-ocr/tessdata
http://www.cnblogs.com/cnlian/p/5765871.html
如何训练自己的字库（traineddata文件）：


Tesseract训练：
大体流程为：安装jTessBoxEditor -> 获取样本文件 -> Merge样本文件 –> 生成BOX文件 
-> 定义字符配置文件 -> 字符矫正 -> 执行批处理文件 -> 将生成的traineddata放入tessdata中



安装jTessBoxEditor
下载jTessBoxEditor，地址https://sourceforge.net/projects/vietocr/files/jTessBoxEditor/；
解压后得到jTessBoxEditor，由于这是由Java开发的，所以我们应该确保在运行jTessBoxEditor前先安装JRE
（Java Runtime Environment，Java运行环境）。



获取样本文件
我们可以用画图工具绘制样本文件，数量越多越好
【注意】：样本图像文件格式必须为tif\tiff格式，否则在Merge样本文件的过程中会出现 Couldn’t Seek 的错误。



Merge样本文件
打开jTessBoxEditor，Tools->Merge TIFF，将样本文件全部选上，并将合并文件保存为all.tif



生成BOX文件
打开命令行并切换至all.tif所在目录，输入tesseract all.tif all nobatch box.train，生成文件名为all.box

tesseract num.font.exp0.tif num.font.exp0 batch.nochop makebox
【语法】：tesseract [lang].[fontname].exp[num].tif [lang].[fontname].exp[num] batch.nochop makebox  
lang为语言名称，fontname为字体名称，num为序号；在tesseract中，一定要注意格式。



定义字符配置文件
在目标文件夹内生成一个名为font_properties的文本文件，内容为all 0 0 0 0 0  
【语法】：<fontname> <italic> <bold> <fixed> <serif> <fraktur>  
fontname为字体名称，italic为斜体，bold为黑体字，fixed为默认字体，serif为衬线字体，
fraktur德文黑字体，1和0代表有和无，精细区分时可使用。



字符矫正
打开jTessBoxEditor，BOX Editor -> Open，打开all.tif，这里jTessBoxEditor会自动打开all.box，
box文件里8 244 1 266 30 0，表示数字8，左右坐标244,266，所以宽度22；
矫正<Char>上的字符，记得<Page>有好多页噢！修改后记得保存。



cmd依次运行：
unicharset_extractor all.box
mftraining -F font_properties -U unicharset all.tr
cntraining all.tr

#把shapetable,normproto,pffmtable,inttemp四个文件前面加上all.，注意有个小数点
然后cmd运行combine_tessdata all就会生成最终的traineddata文件，移动到tesseract的tessdata里即可。
外面有所有文件的截图
'''
