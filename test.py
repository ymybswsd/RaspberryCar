import cv2 as cv

img = cv.imread('/home/pi/lll.jpg')
cv.namedWindow("Image",0)
cv.imshow("Image",img)
cv.waitKey(0)
cv.destroyAllWindows()