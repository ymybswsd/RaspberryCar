import socket
import RPi.GPIO as gpio
import time
import signal
import atexit
import serial
import numpy as np
import pyzbar.pyzbar as pyzbar
import cv2
from shape_detect import shape

width = 320
height = 240
dim = (width,height)
lower_red=np.array([0,115,116])#红色阈值下界
higher_red=np.array([15,255,255])#红色阈值上界
lower_green=np.array([35,110,106])#绿色阈值下界
higher_green=np.array([77,255,255])#绿色阈值上界
lower_blue=np.array([100,43,46])
higher_blue=np.array([124,255,255])

gpio.setmode(gpio.BCM)  # BCM引脚编号模式
gpio.setup(5, gpio.OUT)  # 设置出
gpio.setup(4, gpio.OUT)  # 设置出
# 舵机的控制信号为周期是20ms的脉宽调制（PWM）信号，其中脉冲宽度从0.5ms-2.5ms，相对应舵盘的位置为0－180度，呈线性变化。
# 周期为20ms 就是0.02秒一次  一秒就是50次 频率是50Hz  （计算式：1/0.02=50Hz）
# 脉冲宽度从0.5ms-2.5ms 除以20ms得出占空比 为 2.5% - 12.5%  对应0-180度
# 12.5%-2.5%=10%  180度-0度=180度  10/180 = 0.0555556 %/度   也就是角度每增加1度‘占空比’增加加0.0555556%
# 根据角度算出’占空比‘：’占空比‘等于（2.5+角度*0.0555556） 把0.0555556替换为10/180 算式为（2.5+角度*10/180）

gs90_pwm = gpio.PWM(5, 50)   # 实例  （针脚 ， 50Hz频率  每秒多少次）
gs90_pwm2 = gpio.PWM(4, 50)

# 占空比控制也被称为电控脉宽调制技术
# 简单的控制线路只能实现接通工作元件电路或切断工作元件线路这两种工况，也就是开或关，无论如何是不能够实现一定范围的从渐开到渐闭的无极线性调控。
# 而占空比控制技术却另辟蹊径，通过对以一定频率加在工作元件上的电压信号进行占空比控制，利用控制简单开关电路的接通和关闭的比率大小，
# 实现了对工作元件上的电压信号的电压平均值的控制，从而最终实现了对流经工作元件的电流控制。
gs90_pwm.start(0)  # 占空比 （范围：0.0 - 100.0）  表示在一个周期内，工作时间与总时间的比值
gs90_pwm2.start(0)

# gs90_pwm.ChangeFrequency(100)  # 更新频率 设置新频率，单位为 Hz
# gs90_pwm.ChangeDutyCycle(10)  # 更新占空比 （范围：0.0 - 100.0）  表示在一个周期内，工作时间与总时间的比值
port = "/dev/ttyAMA0"
serr = serial.Serial(port, 115200, timeout=1)  # //打开串口，连接到Arduino上
serr.flushInput()  # //清空输入缓冲区

noise_b = 0.5


def color():
    cap = cv2.VideoCapture(0)
    if(cap.isOpened()):
        while(True):
            ret,img=cap.read()#按帧读取，这是读取一帧
            frame = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
            img_hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            mask_red=cv2.inRange(img_hsv,lower_red,higher_red)#可以认为是过滤出红色部分，获得红色的掩膜
            mask_green=cv2.inRange(img_hsv,lower_green,higher_green)#获得绿色部分掩膜
            mask_blue=cv2.inRange(img_hsv,lower_blue,higher_blue)#获得绿色部分掩膜
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
                return "red"

            for cnt in cnts2:
                (x, y, w, h) = cv2.boundingRect(cnt)  # 该函数返回矩阵四个点
                if w*h<1000:
                    continue
#                 cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 将检测到的颜色框起来
#                 cv2.putText(frame, 'blue', (x, y - 5), font, 0.7, (0,255,0), 2)
                return "blue"
            
            for cnt in cnts3:
                (x, y, w, h) = cv2.boundingRect(cnt)  # 该函数返回矩阵四个点
                if w*h<1000:
                    continue
#                 cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 将检测到的颜色框起来
#                 cv2.putText(frame, 'green', (x, y - 5), font, 0.7, (0,255,0), 2)
                return "green"
            
def erweima2():
    cap = cv2.VideoCapture(0)
    ret,img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    barcodes = pyzbar.decode(gray)
    strlist = ''
    for barcode in barcodes:
        # 提取二维码的位置,然后用边框标识出来在视频中
        (x, y, w, h) = barcode.rect
        # cv2.rectangle(video, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # 字符串转换
        barcodeData = barcode.data.decode("utf-8")
        # print(barcodeData)
        barcodeType = barcode.type
        # 在图像上面显示识别出来的内容
        # text = "{}".format(barcodeData)
        # cv2.putText(video, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # 打印识别后的内容
        strlist = strlist + barcodeData
        # print("[扫描结果] 二维码类别： {0} 内容： {1}".format(barcodeType, barcodeData))
        # cv2.imshow("cam", video)
        # cv2.waitKey(0)
        strlist1 = strlist.split(',')
        return barcodeData

def erweima():
    cap = cv2.VideoCapture(0)
    ret,img = cap.read()
    while True:
        ret, img = cap.read()
        img2 = img.copy()
        kernel = np.ones((30,30),np.uint8)
        erosion = cv2.erode(img,kernel,iterations = 1)
        # cv2.imshow("imgg",erosion)
        imgray=cv2.cvtColor(erosion,cv2.COLOR_BGR2GRAY)
        ret,binary = cv2.threshold(imgray, 50, 255, cv2.THRESH_BINARY_INV)
        # cv2.imshow("binary",binary)
        img,contours,hierarchy=cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        arr = []
        for i in range(len(contours)):
            x, y, w, h = cv2.boundingRect(contours[i])
            if w*h>600 and 0.95<w/h<1.05:
                arr.append(i)
                # cv2.rectangle(img2, (x,y), (x+w,y+h), (0,255,0), 5)
        # print(len(arr))
        if len(arr) == 3:
            x, y, w, h = cv2.boundingRect(contours[arr[0]])
            x1, y1, w1, h1 = cv2.boundingRect(contours[arr[1]])
            x2, y2, w2, h2 = cv2.boundingRect(contours[arr[2]])
            if x2> x > x1 or x2 < x <x1:
                cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 255, 0), 5)
                imger = img2[y:y + h, x:x + w]
            elif x2 > x1 > x or x2 < x1 < x:
                cv2.rectangle(img2, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 5)
                imger = img2[y1:y1 + h1, x1:x1 + w1]
            elif x > x2 > x1 or x < x2 < x1:
                cv2.rectangle(img2, (x2, y2), (x2 + w2, y2 + h2), (0, 255, 0), 5)
                imger = img2[y2:y2 + h2, x2:x2 + w2]
            # cv2.imshow("img3", img2)
        try:
            gray = cv2.cvtColor(imger, cv2.COLOR_BGR2GRAY)
        except:
            continue
        gray = cv2.cvtColor(imger, cv2.COLOR_BGR2GRAY)
        barcodes = pyzbar.decode(gray)
        strlist = ''
        for barcode in barcodes:
            # 提取二维码的位置,然后用边框标识出来在视频中
            (x, y, w, h) = barcode.rect
            # cv2.rectangle(video, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # 字符串转换
            barcodeData = barcode.data.decode("utf-8")
            # print(barcodeData)
            barcodeType = barcode.type
            # 在图像上面显示识别出来的内容
            # text = "{}".format(barcodeData)
            # cv2.putText(video, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            # 打印识别后的内容
            strlist = strlist + barcodeData
            # print("[扫描结果] 二维码类别： {0} 内容： {1}".format(barcodeType, barcodeData))
            # cv2.imshow("cam", video)
            # cv2.waitKey(0)
            strlist1 = strlist.split(',')
            return barcodeData

        # for i in range(len(contours)):
        #     img=cv2.drawContours(img,[contours[i]],-1,(0,255,0),10)
            # print(contours[i])
        # cv2.imshow("img2",img)
        # cv2.waitKey(0)

def gs90_angle(angle):
    '''angle 输入0-180度 如果输入 'stop' 则停止'''
    if isinstance(angle, str):  # 判断数据类型
        if angle.upper() == 'STOP':
            gs90_pwm.ChangeDutyCycle(0)  # 更新占空比 （范围：0.0 - 100.0）  表示在一个周期内，工作时间与总时间的比值
        else:
            print('输入有误')
    elif isinstance(angle, int) or isinstance(angle, float):  # 判断数据类型
        gs90_pwm.ChangeDutyCycle(2.5 + angle * 10 / 180)  # 更新占空比 （范围：0.0 - 100.0）  表示在一个周期内，工作时间与总时间的比值



# 明确配置变量
ip_port = ('192.168.4.3', 8080)
back_log = 5
buffer_size = 1024
# 创建一个TCP套接字
ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 套接字类型AF_INET, socket.SOCK_STREAM   tcp协议，基于流式的协议
ser.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 对socket的配置重用ip和端口号
# 绑定端口号
ser.bind(ip_port)  # 写哪个ip就要运行在哪台机器上
# 设置半连接池
ser.listen(back_log)  # 最多可以连接多少个客户端
while 1:
    # 阻塞等待，创建连接
    print("等待连接")
    con, address = ser.accept()  # 在这个位置进行等待，监听端口号
    while 1:
        try:
            # 接受套接字的大小，怎么发就怎么收
            msg = con.recv(buffer_size)
            if msg.decode('utf-8') == '1':
                # 断开连接
                con.close()
            print('服务器收到消息', msg.decode('utf-8'))
            str = msg.decode('utf-8')
            if (str[0]=='d'):
                str = str[1:]
                num = str.split('d',2)
                numm = []
                print(num)
                numm.append(int(num[0]))
                numm.append(int(num[1]))
                print(numm)
                gs90_pwm.ChangeDutyCycle(2.5 + (180-numm[0]/100*180) * 10 / 180)
                time.sleep(0.1)
                gs90_pwm.ChangeDutyCycle(0)
                gs90_pwm2.ChangeDutyCycle(2.5 + numm[1]/100*180 * 10 / 180)
                time.sleep(0.1)
                gs90_pwm2.ChangeDutyCycle(0)
            elif(str[0]=='g'):
                str = str[1:]
                if str[0] == 'f':
                    print('[')
                    serr.write('f'.encode())
                    print("]")
                elif str[0] == 'b':
                    serr.write('b'.encode())
                elif str[0] == 'l':
                    serr.write('l'.encode())
                elif str[0] == 'r':
                    serr.write('r'.encode())
            elif(str[0]=='l'):
                str = str[1:]
                if str[0] == 'e':
                    ss = erweima2()
                    print(ss)
                    for i in range(len(ss)):
                        serr.write(ss[i].encode())
                elif str[0] == 'j':
                    c1,c5,c6,c9,c13=shape()
                    if c1==1 and c5==0 and c6==0 and c9==0 and c13==0:
                        strx = "Triangle"
                        for i in range(len(strx)):
                            serr.write(strx[i].encode())
                    
                    if c1==0 and c5==1 and c6==0 and c9==0 and c13==0:
                        strx = "Rectangle"
                        for i in range(len(strx)):
                            serr.write(strx[i].encode())
                        
                    if c1==0 and c5==0 and c6==1 and c9==0 and c13==0:
                        strx = "Ling"
                        for i in range(len(strx)):
                            serr.write(strx[i].encode())
                        
                    if c1==0 and c5==0 and c6==0 and c9==1 and c13==0:
                        strx = "Star"
                        for i in range(len(strx)):
                            serr.write(strx[i].encode())
                        
                    if c1==0 and c5==0 and c6==0 and c9==0 and c13==1:
                        strx = "circle"
                        for i in range(len(strx)):
                            serr.write(strx[i].encode())
                        
                    serr.write(chr(c1+48).encode())
                    serr.write(chr(c5+48).encode())
                    serr.write(chr(c6+48).encode())
                    serr.write(chr(c9+48).encode())
                    serr.write(chr(c13+48).encode())
                    print("ok")
                elif str[0] == 'c':
                    colorstr = color()
                    print(colorstr)
                    for i in range(len(colorstr)):
                        serr.write(colorstr[i].encode())

        except Exception as e:
            break
# 关闭服务器
ser.close()
