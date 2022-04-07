import cv2 as cv
import numpy as np
import math
"""
    功能：实现多种几何图形的形状及颜色的识别，并计算面积及周长
    可以识别的图形：三角形，任意四边形（梯形，平行四边形，菱形，正方形，矩形，不特殊四边形），
                    五边形，五角星，六边形，多边形，椭圆，半圆，圆
    可以识别的颜色：红色，绿色，蓝色，黄色，黑色，紫色，橙色，白色
    除了定义的可识别颜色外，其他返回其对应的rgb值，提示用户根据rgb值去找寻相应颜色                 
    除了定义的可识别图形外，其他为未定义的图形  
"""
noise_b = 0.5


class ShapeAnalysis:
    def __init__(self):
        self.shapes = {'triangle': 0,
                       'quadrilateral': 0, 'trapezium': 0, 'parallelogram': 0,
                       'rectangle': 0, 'rhombus': 0, 'square': 0,
                       'pentagon': 0, 'pentagram': 0, 'hexagon': 0,
                       'polygons': 0, 'ellipse': 0, 'circle': 0,
                       'undefined': 0
                       }

        self.colors = {'white': 0, 'black': 0,
                       'red': 0, 'green': 0,
                       'blue': 0, 'yellow': 0,
                       'orange': 0, 'purple': 0,
                       'others': 0
                       }

    def analysis(self, frame):
        self.re_strover = '识别结果：\n'
        h, w, ch = frame.shape  # 获取图形信息
        result = np.zeros((h, w, ch), dtype=np.uint8)  # 生成跟图形相同大小的矩阵
#         cv.imshow("input image", frame)

        # 二值化图像
        print('start to binary image and detect edges...\n')
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # threshold：固定阈值二值化 ret, dst输出图 = cv2.threshold(src输入图, thresh阈值, maxval, type)
        # type：二值化操作的类型，包含以下5种类型： cv2.THRESH_BINARY；
        # cv2.THRESH_BINARY_INV； cv2.THRESH_TRUNC； cv2.THRESH_TOZERO；cv2.THRESH_TOZERO_INV
        # adaptiveThreshold自适应阈值二值化
        ret, binary = cv.threshold(gray, 5, 255, cv.THRESH_BINARY_INV)
#         cv.imshow("bin",binary)
#         cv.waitKey(0)
        kernel = np.ones((3, 3), dtype=np.uint8)
        binary = cv.dilate(binary, kernel, 1)
#         cv.imshow("bin1", binary)
#         cv.waitKey(0)
        # 函数cv2.findContours()有三个参数。第一个是输入图像，第二个是轮廓检索模式，第三个是轮廓近似方法。
        # 轮廓的点集(contours)[Next, Previous, First_Child, Parent]
        # 各层轮廓的索引(hierarchy)
        img,contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        if len(contours) < 1e-6:
            print('there is nothing can be detected! Please check the input image. Thanks！')
        else:
            shape_numbers = 0
            for cnt in range(len(contours)):

                # 通过计算周长和面积来排除一些图像干扰
                # 计算面积与周长
                p = cv.arcLength(contours[cnt], True)
                area = cv.contourArea(contours[cnt])
                if area < h*w*0.003:
                    continue
                if area > noise_b and p > noise_b:  # 如果面积和周长小于0.5判断为噪声干扰，不是图形
                    shape_numbers += 1   # 统计检测到图形

                    # 为图形，做统计分析
                    cv.drawContours(result, contours, cnt, (0, 255, 0), 2)  # 画出轮廓

                    # 求解中心位置
                    mm = cv.moments(contours[cnt])
                    cx = int(mm['m10'] / (mm['m00'] + 1e-12))
                    cy = int(mm['m01'] / (mm['m00'] + 1e-12))
                    cv.circle(result, (cx, cy), 3, (0, 0, 255), -1)
                    # if cx < w*0.2 or cx >w*0.8 or cy < h*0.2 or cy >h*0.8:
                    #     continue

                    # 获取颜色信息
                    color = frame[cy][cx]
                    color_str = "(" + str(color[0]) + ", " + str(color[1]) + ", " + str(color[2]) + ")"

                    global color_type
                    color_type = ""
                    # 颜色匹配分析
                    if (color[0], color[1], color[2]) == (255, 255, 255):
                        count = self.colors['white']
                        count = count + 1
                        self.colors['white'] = count
                        color_type = '白色'
                        cv.putText(result, "white", (cx + 5, cy), cv.FONT_HERSHEY_PLAIN, 0.4, (255, 255, 255),
                                   1)
                    elif (color[0], color[1], color[2]) == (0, 0, 0):
                        count = self.colors['black']
                        count = count + 1
                        self.colors['black'] = count
                        color_type = '黑色'
                        cv.putText(result, "black", (cx + 5, cy), cv.FONT_HERSHEY_PLAIN, 0.4, (255, 255, 255),
                                   1)
                    elif (color[0], color[1], color[2]) == (0, 0, 255):
                        count = self.colors['red']
                        count = count + 1
                        self.colors['red'] = count
                        color_type = '红色'
                        cv.putText(result, "red", (cx + 5, cy), cv.FONT_HERSHEY_PLAIN, 0.4, (255, 255, 255),
                                   1)
                    elif (color[0], color[1], color[2]) == (0, 255, 0):
                        count = self.colors['green']
                        count = count + 1
                        self.colors['green'] = count
                        color_type = '绿色'
                        cv.putText(result, "green", (cx + 5, cy), cv.FONT_HERSHEY_PLAIN, 0.4, (255, 255, 255),
                                   1)
                    elif (color[0], color[1], color[2]) == (255, 0, 0):
                        count = self.colors['blue']
                        count = count + 1
                        self.colors['blue'] = count
                        color_type = '蓝色'
                        cv.putText(result,"blue", (cx + 5, cy), cv.FONT_HERSHEY_PLAIN, 0.4, (255, 255, 255),
                                   1)
                    elif (color[0], color[1], color[2]) == (0, 128, 255):
                        count = self.colors['orange']
                        count = count + 1
                        self.colors['orange'] = count
                        color_type = '橙色'
                        cv.putText(result, "orange", (cx + 5, cy), cv.FONT_HERSHEY_PLAIN, 0.4, (255, 255, 255),
                                   1)
                    elif (color[0], color[1], color[2]) == (0, 255, 255):
                        count = self.colors['yellow']
                        count = count + 1
                        self.colors['yellow'] = count
                        color_type = '黄色'
                        cv.putText(result, "yellow", (cx + 5, cy), cv.FONT_HERSHEY_PLAIN, 0.4, (255, 255, 255),
                                   1)
                    elif (color[0], color[1], color[2]) == (255, 0, 255):
                        count = self.colors['purple']
                        count = count + 1
                        self.colors['purple'] = count
                        color_type = '紫色'
                        cv.putText(result, "purple", (cx + 5, cy), cv.FONT_HERSHEY_PLAIN, 0.4, (255, 255, 255),
                                   1)
                    else:
                        count = self.colors['others']
                        count = count + 1
                        self.colors['others'] = count
                        color_type = color_str
                        cv.putText(result, str(color_type), (cx + 5, cy), cv.FONT_HERSHEY_PLAIN, 0.4, (255, 255, 255), 1)

                    # 轮廓逼近
                    epsilon = 0.01 * cv.arcLength(contours[cnt], True)
                    approx = cv.approxPolyDP(contours[cnt], epsilon, True)

                    # 分析几何形状
                    corners = len(approx)
                    global shape_type
                    shape_type = ""
                    if corners == 3:
                        count = self.shapes['triangle']
                        count = count + 1
                        self.shapes['triangle'] = count
                        shape_type = "三角形"
                        cv.putText(result, "triangle", (cx + 5, cy + 12), cv.FONT_HERSHEY_PLAIN, 0.4,
                                   (255, 255, 255), 1)
                    elif corners == 4:
                        polygon = approx[:, 0, :]
                        s1 = np.linalg.norm(polygon[0] - polygon[1])
                        s2 = np.linalg.norm(polygon[1] - polygon[2])
                        s3 = np.linalg.norm(polygon[2] - polygon[3])
                        s4 = np.linalg.norm(polygon[3] - polygon[0])
                        d1 = np.linalg.norm(polygon[0] - polygon[2])
                        d2 = np.linalg.norm(polygon[1] - polygon[3])

                        if abs(s1 - s3) <= 10 and abs(s2 - s4) <= 10:
                            if abs(s1 - s2) <= 10:
                                if abs(d1 - d2) <= 10:
                                    count = self.shapes['square']
                                    count = count + 1
                                    self.shapes['square'] = count
                                    shape_type = "正方形"
                                    cv.putText(result, "square", (cx + 5, cy + 12), cv.FONT_HERSHEY_PLAIN, 0.4,
                                               (255, 255, 255), 1)
                                else:
                                    count = self.shapes['rhombus']
                                    count = count + 1
                                    self.shapes['rhombus'] = count
                                    shape_type = "菱形"
                                    cv.putText(result, "rhombus", (cx + 5, cy + 12), cv.FONT_HERSHEY_PLAIN, 0.4,
                                               (255, 255, 255), 1)
                            else:
                                if abs(d1 - d2) <= 10:
                                    count = self.shapes['rectangle']
                                    count = count + 1
                                    self.shapes['rectangle'] = count
                                    shape_type = "矩形"
                                    cv.putText(result, "rectangle", (cx + 5, cy + 12), cv.FONT_HERSHEY_PLAIN, 0.4,
                                               (255, 255, 255), 1)
                                else:
                                    count = self.shapes['parallelogram']
                                    count = count + 1
                                    self.shapes['parallelogram'] = count
                                    shape_type = "平行四边形"
                                    cv.putText(result, "parallelogram", (cx + 5, cy + 12), cv.FONT_HERSHEY_PLAIN, 0.4,
                                               (255, 255, 255), 1)
                        else:
                            if abs(math.atan2(s1,s3)) <= 0.8 or abs(math.atan2(s2, s4)) <= 0.8:
                                count = self.shapes['trapezium']
                                count = count + 1
                                self.shapes['trapezium'] = count
                                shape_type = "梯形"
                                cv.putText(result, "trapezium", (cx + 5, cy + 12), cv.FONT_HERSHEY_PLAIN, 0.4,
                                           (255, 255, 255), 1)
                            else:
                                count = self.shapes['quadrilateral']
                                count = count + 1
                                self.shapes['quadrilateral'] = count
                                shape_type = "四边形"
                                cv.putText(result, "quadrilateral", (cx + 5, cy + 12), cv.FONT_HERSHEY_PLAIN, 0.4,
                                           (255, 255, 255), 1)
                    elif corners == 5:
                        count = self.shapes['pentagon']
                        count = count + 1
                        self.shapes['pentagon'] = count
                        shape_type = "五边形"
                        cv.putText(result, "pentagon", (cx + 5, cy + 12), cv.FONT_HERSHEY_PLAIN, 0.4,
                                   (255, 255, 255), 1)
                    elif corners == 6:
                        count = self.shapes['hexagon']
                        count = count + 1
                        self.shapes['hexagon'] = count
                        shape_type = "六边形"
                        cv.putText(result, "hexagon", (cx + 5, cy + 12), cv.FONT_HERSHEY_PLAIN, 0.4,
                                   (255, 255, 255), 1)
                    elif 6 < corners < 9:
                        count = self.shapes['polygons']
                        count = count + 1
                        self.shapes['polygons'] = count
                        shape_type = "多边形"
                        cv.putText(result, "polygons", (cx + 5, cy + 12), cv.FONT_HERSHEY_PLAIN, 0.4,
                                   (255, 255, 255), 1)
                    elif corners == 10:
                        count = self.shapes['pentagram']
                        count = count + 1
                        self.shapes['pentagram'] = count
                        shape_type = "五角星"
                        cv.putText(result, "pentagram", (cx + 5, cy + 12), cv.FONT_HERSHEY_PLAIN, 0.4,
                                   (255, 255, 255), 1)
                    elif 10 < corners <= 14 or corners == 9:
                        count = self.shapes['ellipse']
                        count = count + 1
                        self.shapes['ellipse'] = count
                        shape_type = "椭圆"
                        cv.putText(result, "ellipse", (cx + 5, cy + 12), cv.FONT_HERSHEY_PLAIN, 0.4,
                                   (255, 255, 255), 1)
                    else:
                        ellipse = cv.boxPoints(cv.fitEllipse(contours[cnt]))
                        a = np.linalg.norm(ellipse[0] - ellipse[1])
                        b = np.linalg.norm(ellipse[1] - ellipse[2])
                        # calculate ratio of contour area to ellipse area
                        area_ratio = (np.pi * a * b) / cv.contourArea(contours[cnt])
                        if np.abs(area_ratio) <= 5:
                            count = self.shapes['circle' if np.abs(a - b) <= 10 else 'ellipse']
                            count = count + 1
                            self.shapes['circle' if np.abs(a - b) <= 10 else 'ellipse'] = count
                            shape_type = "圆" if np.abs(a - b) <= 10 else "椭圆"
                            if np.abs(a - b) <= 10:
                                cv.putText(result, "circle", (cx + 5, cy + 12), cv.FONT_HERSHEY_PLAIN, 0.4,
                                           (255, 255, 255), 1)
                            else:
                                cv.putText(result, "ellipse", (cx + 5, cy + 12), cv.FONT_HERSHEY_PLAIN, 0.4,
                                           (255, 255, 255), 1)
                        else:
                            count = self.shapes['undefined']
                            count = count + 1
                            self.shapes['undefined'] = count
                            shape_type = "未定义的图形"
                            cv.putText(result, "undefined", (cx + 5, cy + 12), cv.FONT_HERSHEY_PLAIN, 0.4,
                                       (255, 255, 255), 1)

                    # 显示并绘制检测结果
                    self.re_strover += "检测到的第"+ str(shape_numbers)+"的信息："+ '\n'
                    print("检测到的第"+str(shape_numbers)+"的信息：")
                    self.re_strover += "形状: %s , 颜色: %s , 周长: %.3f, 面积: %.3f " % (shape_type, color_type, p, area) + '\n'
                    print("形状: %s , 颜色: %s , 周长: %.3f, 面积: %.3f " % (shape_type, color_type, p, area))
                    cv.circle(result, (cx, cy), 3, (255, 255, 255), -1)
#             cv.imshow("Analysis Result", self.draw_text_info(result))
#             cv.imwrite("E:\homework_python\RY_Imagedetect_tools\judege-test-result3.png", self.draw_text_info(result))
            self.new_grayimg = self.draw_text_info(result)
            return self.shapes


    def draw_text_info(self,image):
        c1 = self.shapes['triangle']
        c2 = self.shapes['quadrilateral']
        c3 = self.shapes['trapezium']
        c4 = self.shapes['parallelogram']
        c5 = self.shapes['rectangle']
        c6 = self.shapes['rhombus']
        c7 = self.shapes['square']
        c8 = self.shapes['pentagon']
        c9 = self.shapes['pentagram']
        c10 = self.shapes['hexagon']
        c11 = self.shapes['polygons']
        c12 = self.shapes['ellipse']
        c13 = self.shapes['circle']
        c14 = self.shapes['undefined']
        cv.putText(image, "triangle: "+str(c1), (10, 20), cv.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 0), 1)
        # cv.putText(image, "quadrilateral: " + str(c2//2), (10, 40), cv.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 0), 1)
        # cv.putText(image, "trapezium: " + str(c3//2), (10, 60), cv.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 0), 1)
        # cv.putText(image, "parallelogram: " + str(c4//2), (10, 80), cv.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 0), 1)
        cv.putText(image, "rectangle: " + str(c5), (10, 100), cv.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 0), 1)
        cv.putText(image, "ling" + str(c6), (10, 120), cv.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 0), 1)
        # cv.putText(image, "square: " + str(c7//2), (10, 140), cv.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 0), 1)
        # cv.putText(image, "pentagon: " + str(c8//2), (10, 160), cv.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 0), 1)
        cv.putText(image, "star: " + str(c9), (10, 180), cv.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 0), 1)
        # cv.putText(image, "hexagon: " + str(c10//2), (10, 200), cv.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 0), 1)
        # cv.putText(image, "polygons: " + str(c11//2), (10, 220), cv.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 0), 1)
        # cv.putText(image, "ellipse: " + str(c12//2), (10, 240), cv.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 0), 1)
        cv.putText(image, "circle: " + str(c13), (10, 260), cv.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 0), 1)
        cv.putText(image, "undefined : " + str(c14), (10, 280), cv.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 0), 1)
        return c1,c5,c6,c9,c13,c14

def shape():
    cap = cv.VideoCapture(0)
    ret,src = cap.read()
#     cv.imshow("src",src)
    ld = ShapeAnalysis()
    ld.analysis(src)
    c1,c5,c6,c9,c13,c14 = ld.draw_text_info(src)
    return c1,c5,c6,c9,c13
