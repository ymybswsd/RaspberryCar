import numpy as np
import cv2

width = 320
height = 240
dim = (width,height)
font= cv2.FONT_HERSHEY_SIMPLEX
lower_red=np.array([0,115,116])#红色阈值下界
higher_red=np.array([15,255,255])#红色阈值上界
lower_green=np.array([35,110,106])#绿色阈值下界
higher_green=np.array([77,255,255])#绿色阈值上界
lower_blue=np.array([100,43,46])#蓝色阈值上届
higher_blue=np.array([124,255,255])#蓝色阈值下界
lower_yellow=np.array([24,33,34])#yellow
higher_yellow=np.array([34,255,255])
lower_qing=np.array([77,43,46])#qing
higher_qing=np.array([99,255,255])
lower_zi=np.array([125,43,46])#zi
higher_zi=np.array([155,255,255])
lower_black=np.array([0,0,0])
higher_black=np.array([127,255,68])

cap=cv2.VideoCapture(0)#打开电脑内置摄像头
def color(cap):
    if(cap.isOpened()):
        while(True):
            ret,img=cap.read()#按帧读取，这是读取一帧
            frame = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
            img_hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            mask_red=cv2.inRange(img_hsv,lower_red,higher_red)#可以认为是过滤出红色部分，获得红色的掩膜
            mask_green=cv2.inRange(img_hsv,lower_green,higher_green)#获得绿色部分掩膜
            mask_blue=cv2.inRange(img_hsv,lower_blue,higher_blue)#获得蓝色部分掩膜
    #         mask_yellow=cv2.inRange(img_hsv,lower_yellow,higher_yellow)#获得绿色部分掩膜
    #         mask_qing=cv2.inRange(img_hsv,lower_qing,higher_qing)#获得绿色部分掩膜
    #         mask_zi=cv2.inRange(img_hsv,lower_zi,higher_zi)#获得绿色部分掩膜
    #         mask_black=cv2.inRange(img_hsv,lower_black,higher_black)#获得绿色部分掩膜
            
            mask_green = cv2.medianBlur(mask_green, 7)  # 中值滤波
            mask_red = cv2.medianBlur(mask_red, 7)  # 中值滤波
            mask_blue = cv2.medianBlur(mask_blue, 7)  # 中值滤波
    #         mask_yellow = cv2.medianBlur(mask_yellow, 7)  # 中值滤波
    #         mask_qing = cv2.medianBlur(mask_qing, 7)  # 中值滤波
    #         mask_zi = cv2.medianBlur(mask_zi, 7)  # 中值滤波
    #         mask_black = cv2.medianBlur(mask_black, 7)  # 中值滤波
    #         
            mask=cv2.bitwise_or(mask_green,mask_red)#三部分掩膜进行按位或运算
            mask=cv2.bitwise_or(mask_green,mask_blue)#三部分掩膜进行按位或运算
    #         mask=cv2.bitwise_or(mask_green,mask_yellow)#三部分掩膜进行按位或运算
    #         mask=cv2.bitwise_or(mask_green,mask_qing)#三部分掩膜进行按位或运算
    #         mask=cv2.bitwise_or(mask_green,mask_zi)#三部分掩膜进行按位或运算
    #         mask=cv2.bitwise_or(mask_green,mask_black)#三部分掩膜进行按位或运算
    #         
            image1,cnts1,hierarchy1=cv2.findContours(mask_red,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)#轮廓检测
            image3,cnts3,hierarchy3=cv2.findContours(mask_green,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
            image2,cnts2,hierarchy2=cv2.findContours(mask_blue,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    #         image4,cnts4,hierarchy4=cv2.findContours(mask_yellow,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    #         image5,cnts5,hierarchy5=cv2.findContours(mask_qing,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    #         image6,cnts6,hierarchy6=cv2.findContours(mask_zi,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    #         image7,cnts7,hierarchy7=cv2.findContours(mask_black,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

            for cnt in cnts1:
                (x,y,w,h)=cv2.boundingRect(cnt)#该函数返回矩阵四个点
                if w*h<1000:
                    continue
#                 cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)#将检测到的颜色框起来
#                 cv2.putText(frame,'red',(x,y-5),font,0.7,(0,0,255),2)
                return "Red"

            for cnt in cnts2:
                (x, y, w, h) = cv2.boundingRect(cnt)  # 该函数返回矩阵四个点
                if w*h<1000:
                    continue
#                 cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 将检测到的颜色框起来
#                 cv2.putText(frame, 'blue', (x, y - 5), font, 0.7, (0,255,0), 2)
                return "Blue"
            
            for cnt in cnts3:
                (x, y, w, h) = cv2.boundingRect(cnt)  # 该函数返回矩阵四个点
                if w*h<1000:
                    continue
#                 cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 将检测到的颜色框起来
#                 cv2.putText(frame, 'green', (x, y - 5), font, 0.7, (0,255,0), 2)
                return "Green"
            
    #         for cnt in cnts4:
    #             (x, y, w, h) = cv2.boundingRect(cnt)  # 该函数返回矩阵四个点
    #             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 将检测到的颜色框起来
    #             cv2.putText(frame, 'yellow', (x, y - 5), font, 0.7, (0,255,0), 2)
    #         
    #         for cnt in cnts5:
    #             (x, y, w, h) = cv2.boundingRect(cnt)  # 该函数返回矩阵四个点
    #             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 将检测到的颜色框起来
    #             cv2.putText(frame, 'qing', (x, y - 5), font, 0.7, (0,255,0), 2)
    #         
    #         for cnt in cnts6:
    #             (x, y, w, h) = cv2.boundingRect(cnt)  # 该函数返回矩阵四个点
    #             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 将检测到的颜色框起来
    #             cv2.putText(frame, 'zi', (x, y - 5), font, 0.7, (0,255,0), 2)
    #             
    #         for cnt in cnts7:
    #             (x, y, w, h) = cv2.boundingRect(cnt)  # 该函数返回矩阵四个点
    #             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 将检测到的颜色框起来
    #             cv2.putText(frame, 'black', (x, y - 5), font, 0.7, (0,255,0), 2)        
    #         
colorstr = color(cap)
print(colorstr)
