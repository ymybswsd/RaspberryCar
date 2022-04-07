import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
cap = cv2.VideoCapture(0)
ret,img = cap.read()
while True:
    ret, img = cap.read()
    img2 = img
    kernel = np.ones((30,30),np.uint8)
    erosion = cv2.erode(img,kernel,iterations = 1)
    cv2.imshow("imgg",erosion)
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
        cv2.imshow("img3", img2)
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
        print(strlist1)

    # for i in range(len(contours)):
    #     img=cv2.drawContours(img,[contours[i]],-1,(0,255,0),10)
        # print(contours[i])
    # cv2.imshow("img2",img)
    cv2.waitKey(1)
