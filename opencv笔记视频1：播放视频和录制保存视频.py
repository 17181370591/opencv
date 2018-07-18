'''
#播放视频
cap.get(i)可以获取视频信息：
Property identifier. It can be one of the following:

CV_CAP_PROP_POS_MSEC Current position of the video file in milliseconds or video capture timestamp.
视频文件的当前位置以毫秒为单位或视频捕获时间戳。

CV_CAP_PROP_POS_FRAMES 0-based index of the frame to be decoded/captured next.
将要解码/捕获的帧的基于0的索引。

CV_CAP_PROP_POS_AVI_RATIO Relative position of the video file: 0 - start of the film,
1 - end of the film.
视频文件的相对位置：0 -电影的开始，1结束的电影。

CV_CAP_PROP_FRAME_WIDTH Width of the frames in the video stream.
视频宽度

CV_CAP_PROP_FRAME_HEIGHT Height of the frames in the video stream.
视频高度

CV_CAP_PROP_FPS Frame rate.
帧速率。

CV_CAP_PROP_FOURCC 4-character code of codec.
4字符编码编解码器。

CV_CAP_PROP_FRAME_COUNT Number of frames in the video file.
视频文件中的帧数。

CV_CAP_PROP_FORMAT Format of the Mat objects returned by retrieve() .
Read（）返回的Mat对象的格式


CV_CAP_PROP_MODE Backend-specific value indicating the current capture mode.
CV_CAP_PROP_BRIGHTNESS Brightness of the image (only for cameras).
CV_CAP_PROP_CONTRAST Contrast of the image (only for cameras).
CV_CAP_PROP_SATURATION Saturation of the image (only for cameras).
CV_CAP_PROP_HUE Hue of the image (only for cameras).
CV_CAP_PROP_GAIN Gain of the image (only for cameras).
CV_CAP_PROP_EXPOSURE Exposure (only for cameras).
CV_CAP_PROP_CONVERT_RGB Boolean flags indicating whether images should be converted to RGB.
CV_CAP_PROP_WHITE_BALANCE_U The U value of the whitebalance setting (note: 
                                    only supported by DC1394 v 2.x backend currently)
CV_CAP_PROP_WHITE_BALANCE_V The V value of the whitebalance setting (note:
                                    only supported by DC1394 v 2.x backend currently)
CV_CAP_PROP_RECTIFICATION Rectification flag for stereo cameras (note:
                                    only supported by DC1394 v 2.x backend currently)
CV_CAP_PROP_ISO_SPEED The ISO speed of the camera (note: 
                                    only supported by DC1394 v 2.x backend currently)
CV_CAP_PROP_BUFFERSIZE Amount of frames stored in internal buffer memory (note: 
                                    only supported by DC1394 v 2.x backend currently)
'''

import numpy as np
import cv2,time

cap = cv2.VideoCapture("1.mp4")

while(1):
    # get a frame
    ret, frame = cap.read()
    # show a frame
    cv2.imshow("capture", frame)
    k=cv2.waitKey(100)                                   #修改每一帧的间隔时间，数值越小播放速度越快

    #按q退出播放，按c截图
    if k & 0xFF == ord('q'):                      
        break
    elif k & 0xFF == ord('c'):
        cv2.imwrite('{}.jpg'.format(time.time()),frame)
    
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()




#====================================================================================

import cv2
#下面是从摄像头捕捉实时流并将其写入文件的Python实现。运行程序后 按键Q推出，按键C进行拍照并保存到当前的路径

# Create a VideoCapture object
cap = cv2.VideoCapture(0)

# Check if camera opened successfully
if not cap.isOpened():
    print("Unable to read camera feed")
    print(cap)
    
# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
# 默认分辨率取决于系统。 我们将分辨率从float转换为整数。这里的cap.get详情见最前面
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
print((frame_width, frame_height))

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
# 定义编解码器并创建VideoWriter对象。输出存储在“outpy.avi”文件中。
#这里的参数1好像是表示自动选择编码器？
out = cv2.VideoWriter('2.mp4', -1,10, (frame_width, frame_height))

index = 0
while True:
    ret, frame = cap.read()
    if ret:
        # Write the frame into the file 'output.avi'
        out.write(frame)

        # Display the resulting frame
        cv2.imshow('frame', frame)

        key = cv2.waitKey(100)
        # Press Q on keyboard to stop recording
        if key & 0xFF == ord('q'):
            break
        if key & 0xFF == ord('c'):
            index += 1
            cv2.imwrite("capture_image_{}.{}".format(index, "jpg"), frame)

    # Break the loop
    else:
        break

# When everything done, release the video capture and video write objects
cap.release()
out.release()

# Closes all the frames
cv2.destroyAllWindows()

