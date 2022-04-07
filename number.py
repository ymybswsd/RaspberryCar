import cv2
import numpy as np
import time

width = 320
height = 240
dim = (width,height)

def aHash(img):
    # 缩放为8*8
#     cv2.imshow("imwe",img)
    img = cv2.resize(img, (16, 16), interpolation=cv2.INTER_CUBIC)
#     cv2.imshow("imggg",img)
#     cv2.waitKey(0)
    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # s为像素和初值为0，hash_str为hash值初值为''
    s = 0
    hash_str = ''
    # 遍历累加求像素和
    for i in range(16):
        for j in range(16):
            s = s + gray[i, j]
    # 求平均灰度
    avg = s / 256
    # 灰度大于平均值为1相反为0生成图片的hash值
    for i in range(16):
        for j in range(16):
            if gray[i, j] > avg:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str


# 差值感知算法
def dHash2(img):
    # 缩放8*8
    img = cv2.resize(img, (17, 16), interpolation=cv2.INTER_CUBIC)
    # 转换灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hash_str = ''
    # 每行前一个像素大于后一个像素为1，相反为0，生成哈希
    for i in range(16):
        for j in range(16):
            if gray[i, j] > gray[i, j + 1]:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str


# Hash值对比
def cmpHash(hash1, hash2):
    n = 0
    # hash长度不同则返回-1代表传参出错
    if len(hash1) != len(hash2):
        return -1
    # 遍历判断
    for i in range(len(hash1)):
        # 不相等则n计数+1，n最终为相似度
        if hash1[i] != hash2[i]:
            n = n + 1
    return n

def number():
    imgyb1 = cv2.imread(r"/home/pi/Desktop/num/0.jpg")
    imgyb2 = cv2.imread(r"/home/pi/Desktop/num/1.jpg")
    imgyb3 = cv2.imread(r"/home/pi/Desktop/num/2.jpg")
    imgyb4 = cv2.imread(r"/home/pi/Desktop/num/3.jpg")
    imgyb5 = cv2.imread(r"/home/pi/Desktop/num/4.jpg")
    imgyb6 = cv2.imread(r"/home/pi/Desktop/num/5.jpg")
    imgyb7 = cv2.imread(r"/home/pi/Desktop/num/6.jpg")
    imgyb8 = cv2.imread(r"/home/pi/Desktop/num/7.jpg")
    imgyb9 = cv2.imread(r"/home/pi/Desktop/num/8.jpg")
    imgyb10 = cv2.imread(r"/home/pi/Desktop/num/9.jpg")
    cap = cv2.VideoCapture(0)
    while True:
        ret,img = cap.read()
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        imgb = img.copy()
        y1 = img.shape[0]
        x1 = img.shape[1]
        # print(x1,y1)
        frame = cv2.medianBlur(img, 5)
#         cv2.imshow("img",frame)
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         cv2.imshow("img2",imgGray)
        ret, binary = cv2.threshold(imgGray, 100, 255, cv2.THRESH_BINARY_INV)
#         cv2.imshow("gg",binary)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 定义结构元素的形状和大小
        dst = cv2.dilate(binary, kernel)  # 膨胀操作
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 8))
        # dst = cv2.dilate(imgGray, kernel)
#         cv2.imshow("dst",dst)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))  # 定义结构元素的形状和大小
        dst = cv2.erode(dst, kernel)  # 腐蚀操作
        imgCanny = cv2.Canny(dst, 250, 250)
#         cv2.imshow("imgCanny", imgCanny)
        img,contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        s = 0
        sign = 0
        for i in range(len(contours)):
            x, y, w, h = cv2.boundingRect(contours[i])
            if w<x1*0.2 or h<y1*0.2:
                continue
            if w*h>2000 and x1*0.2<w<x1*0.8 and y1*0.2<h<y1*0.8:
                if w * h > s:
                    s = w * h
                    sign = i
        x, y, w, h = cv2.boundingRect(contours[sign])
        # cv2.rectangle(img, (x+int(w*0.05),y+int(h*0.05)), (x+w-int(w*0.05),y+h-int(h*0.05)), (0,255,0), 5)
        img2 = imgb[y+int(h*0.08):y+h-int(h*0.1), x+int(w*0.2):x+w-int(w*0.2)]
        img3 = imgb[y:y+h, x:x+w]
#         cv2.imshow("img222",img2)
#         cv2.imwrite("/home/pi/Desktop/num/8.jpg",img2)
#         cv2.waitKey(0)
        hash0 = aHash(img2)
        hash1 = aHash(imgyb1)
        hash2 = aHash(imgyb2)
        hash3 = aHash(imgyb3)
        hash4 = aHash(imgyb4)
        hash5 = aHash(imgyb5)
        hash6 = aHash(imgyb6)
        hash7 = aHash(imgyb7)
        hash8 = aHash(imgyb8)
        hash9 = aHash(imgyb9)
        hash10 = aHash(imgyb10)
        n = cmpHash(hash0, hash1)
        n2 = cmpHash(hash0, hash2)
        n3 = cmpHash(hash0, hash3)
        n4 = cmpHash(hash0, hash4)
        n5 = cmpHash(hash0, hash5)
        n6 = cmpHash(hash0, hash6)
        n7 = cmpHash(hash0, hash7)
        n8 = cmpHash(hash0, hash8)
        n9 = cmpHash(hash0, hash9)
        n10 = cmpHash(hash0, hash10)
        arr = []
        arr.append(n)
        arr.append(n2)
        arr.append(n3)
        arr.append(n4)
        arr.append(n5)
        arr.append(n6)
        arr.append(n7)
        arr.append(n8)
        arr.append(n9)
        arr.append(n10)
        arr.sort()
        print("arr[0]",arr[0])
        if arr[0]<45:
            if arr[0] == n:
                print("0")
                return 0
            elif arr[0] == n2:
                print("1")
                return 1
            elif arr[0] == n3:
                print("2")
                return 2
            elif arr[0] == n4:
                print("3")
                return 3
            elif arr[0] == n5:
                print("4")
                return 4
            elif arr[0] == n6:
                print("5")
                return 5
            elif arr[0] == n7:
                print("6")
                return 6
            elif arr[0] == n8:
                print("7")
                return 7
            elif arr[0] == n9:
                print("8")
                return 8
            elif arr[0] == n10:
                print("9")
                return 9
#         cv2.imshow("img",img2)
        cv2.waitKey(1)
