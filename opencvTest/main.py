import cv2
import numpy as np

cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture("http://192.168.16.130:81/videostream.cgi?user=admin&pwd=888888")
ret,img = cap.read()

# for i in range(0,1000):
#     k = np.random.randint(0,500)
#     j = np.random.randint(0,500)
#     for g in range(0,3):
#         img.itemset((k,j,g),255)
# imgblur = img
# imgGauss = img
# imgMedianblur = img
# imgblur = cv2.blur(imgblur,(3,3))
# imgGauss = cv2.GaussianBlur(imgGauss,(5,5),1)
# imgMedianblur = cv2.medianBlur(imgMedianblur,5)
# margeimg = np.hstack((imgblur,imgGauss,imgMedianblur))
# cv2.imshow("img",margeimg)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# img2 = img
# img3 = img+img2
# img4 = cv2.add(img,img2)
# imgMarge = np.hstack((img3,img4))
# print(img[0:20,:1])
# print("##############")
# print(img2[0:20,:1])
# print("###############")
# print(img4[0:20,:1])
# cv2.imshow("img",imgMarge)

# img2 = img + 200
# img3 = cv2.add(img,200)
# print(img[0:10,:1])
# print("***********")
# print(img2[0:10,:1])
# print(img3[0:10,:1])
# ret,img = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
# cv2.imshow("img1",img)
# kernel = np.ones((5,5),np.uint8)
# erosionImg = cv2.erode(img,kernel,iterations=1)
# cv2.imshow("erosion",erosionImg)
# dilate = cv2.dilate(erosionImg,kernel,iterations=1)
# cv2.imshow("dilate",dilate)

# ret,img = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
# kernel = np.ones((5,5),np.uint8)
# img2 = img
# cv2.imshow("img2",img)
# erosionImg = cv2.erode(img,kernel,iterations=1)
# dilateImd = cv2.dilate(erosionImg,kernel,iterations=1)
# img = cv2.morphologyEx(img,cv2.MORPH_OPEN,kernel)
# cv2.imshow("img",img)
# cv2.imshow("erosion",dilateImd)

# img[:,:,0]=0
# img[:,:,2]=0
# cv2.imshow("img",img)

# flip = cv2.flip(img,1)
# cv2.imshow("img",flip)
# cv2.imshow("img2",img)
# img = cv2.imread("C:\\Users\\24522\\Desktop\\xingzhang.jpg")
#
def nothing(x):
    pass

cv2.namedWindow("TrackBar")
cv2.createTrackbar("L-H","TrackBar",0,255,nothing)
cv2.createTrackbar("L-S","TrackBar",0,255,nothing)
cv2.createTrackbar("L-V","TrackBar",0,255,nothing)
cv2.createTrackbar("H-H","TrackBar",30,255,nothing)
cv2.createTrackbar("H-S","TrackBar",255,255,nothing)
cv2.createTrackbar("H-V","TrackBar",255,255,nothing)

while True:
    ret,img = cap.read()
    cv2.imshow("img",img)
    img2 = cv2.medianBlur(img,5)
    hsv = cv2.cvtColor(img2,cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("L-H","TrackBar")
    l_s = cv2.getTrackbarPos("L-S","TrackBar")
    l_v = cv2.getTrackbarPos("L-V","TrackBar")
    h_h = cv2.getTrackbarPos("H-H","TrackBar")
    h_s = cv2.getTrackbarPos("H-S","TrackBar")
    h_v = cv2.getTrackbarPos("H-V","TrackBar")


    low_red = np.array([l_h,l_s,l_v])
    hei_red = np.array([h_h,h_s,h_v])

    mask = cv2.inRange(hsv,low_red,hei_red)
    cv2.imshow("mask",mask)
    img,contours,f= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    print(len(contours))
    for cnt in contours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        x =approx.ravel()[0]
        y =approx.ravel()[1]
        if area > 400:
            cv2.drawContours(img,[approx],0,(0,0,0),5)
            if len(approx) == 4:
                cv2.putText(img,"Rectangle",(x,y),cv2.FONT_HERSHEY_COMPLEX_SMALL,2,(0,255,0))
            if len(approx) == 3:
                cv2.putText(img,"triangle",(x,y),cv2.FONT_HERSHEY_COMPLEX_SMALL,2,(0,255,0))
            if len(approx) >12:
                 cv2.putText(img,"circle",(x,y),cv2.FONT_HERSHEY_COMPLEX_SMALL,2,(0,255,0))
    
    if cv2.waitKey(1)==ord('q'):
        break
# img = cv2.imread("C:\\Users\\24522\\Documents\\Tencent Files\\2452207447\\FileRecv\\MobileFile\\red.jpg")
#
#
# img2 = cv2.medianBlur(img,3)
# hsv = cv2.cvtColor(img2,cv2.COLOR_BGR2HSV)
#
# low_red = np.array([0,100,100])
# hei_red = np.array([10,255,255])
#
# mask = cv2.inRange(hsv,low_red,hei_red)
# contours,f= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
# for cnt in contours:
#     area = cv2.contourArea(cnt)
#     approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
#     x =approx.ravel()[0]
#     y =approx.ravel()[1]
#     if area > 400:
#         cv2.drawContours(img,[approx],0,(0,0,0),2)
#         if len(approx) == 4:
#             cv2.putText(img,"Rectangle",(x,y),cv2.FONT_HERSHEY_COMPLEX_SMALL,2,(0,255,0))
#         if len(approx) == 3:
#             cv2.putText(img,"triangle",(x,y),cv2.FONT_HERSHEY_COMPLEX_SMALL,2,(0,255,0))
#         if len(approx) >12:
#             cv2.putText(img,"circle",(x,y),cv2.FONT_HERSHEY_COMPLEX_SMALL,2,(0,255,0))
# cv2.imshow("img",img)
# if cv2.waitKey(0)==ord('q'):
cv2.destroyAllWindows()