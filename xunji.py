import cv2
import numpy
import serial
import time
from number import number

port = "/dev/ttyAMA0"
serr = serial.Serial(port, 115200, timeout=1)  # //打开串口，连接到Arduino上
serr.flushInput()  # //清空输入缓冲区

width = 320
height = 240
dim = (width,height)

def panduan(binary):
    num = 0
    for i in range(len(binary)):
            if binary[i][90] == 255:
                num += 1
    if num > 120:
        return 1
    else:
        return 0

def panduan2(binary):
    num = 0
    for i in range(len(binary)):
            if binary[i][10] == 255:
                num += 1
    if num > 120:
        return 1
    else:
        return 0

def panduan3(binary):
    for i in range(len(binary)):
            if binary[230][i] == 0:
                return 0
    return 1

numshizi = 0
num = number()
serr.write(chr(num).encode())ls

while True:
    cap = cv2.VideoCapture(0)
    while True:
            print("num="+num)
            ret,img = cap.read()
            img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, binary = cv2.threshold(imgGray, 140, 255, cv2.THRESH_BINARY_INV)
#             cv2.imshow("binary",binary)
            if (panduan(binary)):
                serr.write('l'.encode())
            if (panduan2(binary)):
#                 print("world")
                serr.write('r'.encode())
            if panduan3(binary):
                if num == 1:
                    serr.write('!'.encode())
                    print("!")
                    time.sleep(2)
                    cap.release()
                    break
                elif num == 2:
                    serr.write('@'.encode())
                    print("@")
                    time.sleep(2)
                    cap.release()
                    break
                elif num == 3:
                    if numshizi == 0:
                        serr.write('#'.encode())
                        print("#")
                        print("hello")
                        time.sleep(2)
                        cap.release()
                        break
                    elif numshizi == 1:
                        serr.write('!'.encode())
                        print("!")
                        time.sleep(2)
                        cap.release()
                        break
                elif num == 4:
                    if numshizi == 0:
                        serr.write('#'.encode())
                        print("#")
                        time.sleep(2)
                        cap.release()
                        break
                    elif numshizi == 1:
                        serr.write('@'.encode())
                        print("@")
                        time.sleep(2)
                        cap.release()
                        break
                elif num == 5:
                    if numshizi == 0 or numshizi == 1:
                        serr.write('#'.encode())
                        print("#")
                        time.sleep(2)
                        cap.release()
                        break
                    elif numshizi == 2:
                        serr.write('!'.encode())
                        print("!")
                        time.sleep(2)
                        cap.release()
                        break
                    if numshizi == 3:
                        serr.write('@'.encode())
                        print("@")
                        time.sleep(2)
                        cap.release()
                        break
                elif num == 7:
                    if numshizi == 0 or numshizi == 1:
                        serr.write('#'.encode())
                        print("#")
                        time.sleep(2)
                        cap.release()
                        break
                    elif numshizi == 2:
                        serr.write('!'.encode())
                        print("!")
                        time.sleep(2)
                        cap.release()
                        break
                    if numshizi == 3:
                        serr.write('!'.encode())
                        print("!")
                        time.sleep(2)
                        cap.release()
                        break
                elif num == 6:
                    if numshizi == 0 or numshizi == 1:
                        serr.write('#'.encode())
                        print("#")
                        time.sleep(2)
                        cap.release()
                        break
                    elif numshizi == 2:
                        serr.write('!'.encode())
                        print("!")
                        time.sleep(2)
                        cap.release()
                        break
                    if numshizi == 3:
                        serr.write('@'.encode())
                        print("@")
                        time.sleep(2)
                        cap.release()
                        break
                elif num == 6:
                    if numshizi == 0 or numshizi == 1:
                        serr.write('#'.encode())
                        print("#")
                        time.sleep(2)
                        cap.release()
                        break
                    elif numshizi == 2:
                        serr.write('!'.encode())
                        print("!")
                        time.sleep(2)
                        cap.release()
                        break
                    if numshizi == 3:
                        serr.write('!'.encode())
                        print("!")
                        time.sleep(2)
                        cap.release()
                        break
            cv2.waitKey(1)
