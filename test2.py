from PIL import Image
import pytesseract
import copy

# TODO ：试试 https://github.com/junmo1215/nctu_portal/blob/master/helper.py
# https://blog.csdn.net/weixin_40267472/article/details/81979379

# def binarizing(img, threshold):
#       """ 传入 image 对象进行灰度、二值处理 """
#       img = img.convert("L")  # 转灰度
#       pixdata = img.load()
#       w, h = img.size
#       if threshold > 0 :
#         # 遍历所有像素，大于阈值的为黑色
#         for y in range(h):
#             for x in range(w):
#                 if pixdata[x, y] < threshold:
#                     pixdata[x, y] = 0
#                 else:
#                     pixdata[x, y] = 255
#       return img


# def depoint(img):
#       """ 传入二值化后的图片进行降噪 """
#       pixdata = img.load()
#       w, h = img.size
#       for y in range(1, h - 1):
#           for x in range(1, w - 1):
#               count = 0
#               if pixdata[x, y - 1] > 245:  # 上
#                   count = count + 1
#               if pixdata[x, y + 1] > 245:  # 下
#                   count = count + 1
#               if pixdata[x - 1, y] > 245:  # 左
#                   count = count + 1
#               if pixdata[x + 1, y] > 245:  # 右
#                   count = count + 1
#               if pixdata[x - 1, y - 1] > 245:  # 左上
#                   count = count + 1
#               if pixdata[x - 1, y + 1] > 245:  # 左下
#                   count = count + 1
#               if pixdata[x + 1, y - 1] > 245:  # 右上
#                   count = count + 1
#               if pixdata[x + 1, y + 1] > 245:  # 右下
#                   count = count + 1
#               if count > 4:
#                   pixdata[x, y] = 255
#       return img

# def del_noise(img,number):
#     height = img.shape[0]
#     width = img.shape[1]

#     img_new = copy.deepcopy(img)
#     for i in range(1, height - 1):
#         for j in range(1, width - 1):
#             point = [[], [], []]
#             count = 0
#             point[0].append(img[i - 1][j - 1])
#             point[0].append(img[i - 1][j])
#             point[0].append(img[i - 1][j + 1])
#             point[1].append(img[i][j - 1])
#             point[1].append(img[i][j])
#             point[1].append(img[i][j + 1])
#             point[2].append(img[i + 1][j - 1])
#             point[2].append(img[i + 1][j])
#             point[2].append(img[i + 1][j + 1])
#             for k in range(3):
#                 for z in range(3):
#                     if point[k][z] == 0:
#                         count += 1
#             if count <= number:
#                 img_new[i, j] = 255
#     return img_new


# # 读取验证码图片
# image = Image.open('/Users/linling/Desktop/e.png')
# imag=binarizing(image, -1)
# # imag=del_noise(image,6)
# imag.show()

# text = pytesseract.image_to_string(image)
# print('识别结果:', text)



#可用于灰度图，二值图的干扰线，噪点去除
# import cv2
# def interference_line(img,thresholdValue,BackColor):#img为源矩阵图，thresholdValue为背景色最小值(颜色最深)BackColor为背景色(一般为白色255)
#     h, w = img.shape[:2]
#     # opencv矩阵点是反的
#     # img[1,2] 1:图片的高度，2：图片的宽度
#     for y in range(1, w -1 ):
#         for x in range(1, h - 1):
#             count = 0
#             if img[x - 1, y - 1].any() > thresholdValue:  # 左上
#                 count = count + 1
#             if img[x - 1, y].any() > thresholdValue:  # 上
#                 count = count + 1
#             if img[x - 1, y + 1].any() > thresholdValue:  # 右上
#                 count = count + 1
#             if img[x, y + 1].any() > thresholdValue:  # 右
#                 count = count + 1
#             if img[x + 1, y + 1].any() > thresholdValue:  # 右下
#                 count = count + 1
#             if img[x + 1, y].any() > thresholdValue:  # 下
#                 count = count + 1
#             if img[x + 1, y - 1].any() > thresholdValue:  # 左下
#                 count = count + 1
#             if img[x, y - 1].any() > thresholdValue:  # 左
#                 count = count + 1
#             if count >= 5:
#                 img[x, y] =BackColor#color值可写为背景色，或者想要转换成的颜色，判断一圈有多少是背景色的，超过5，就转成我们想要的背景色的。
#     cv2.imwrite('/Users/linling/Desktop/result.png',img)#效果图路径
#     return img

# img=cv2.imread('/Users/linling/Desktop/e.png')#源图片路径
# cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)#灰度处理
# interference_line(img,200,255)
    