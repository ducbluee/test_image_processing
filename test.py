import cv2
import numpy as np
import imutils
from matplotlib import pyplot as plt
import pandas as pd
import xlsxwriter
from pandas import DataFrame
import time


a = time.time()
def sort_contours(cnts, method="left-to-right"):
    # initialize the reverse flag and sort index
    reverse = False
    i = 0

    # handle if we need to sort in reverse
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True

    # handle if we are sorting against the y-coordinate rather than
    # the x-coordinate of the bounding box
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1

    # construct the list of bounding boxes and sort them from top to
    # bottom
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
        key=lambda b:b[1][i], reverse=reverse))

    # return the list of sorted contours and bounding boxes
    return (cnts)


img = cv2.imread('t1.png')
# cv2.imshow('img', img)
# cv2.waitKey(0)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2.imshow('1', gray)
# cv2.waitKey(0)


im_width = gray.shape[1]
im_height = gray.shape[0]

up_img = gray[int(0.12*im_height):int(0.34*im_height), int(0.68*im_width):int(0.92*im_width)]
cv2.imshow('2',up_img)
cv2.waitKey(0)
down_img_right = gray[int(0.41*im_height):int(0.92*im_height), int(0.6*im_width):int(0.8*im_width)]
# cv2.imshow('2',down_img_right)
# cv2.waitKey(0)
down_img_left = gray[int(0.41*im_height):int(0.92*im_height), int(0.18*im_width):int(0.38*im_width)]
# cv2.imshow('2',down_img_left)
# cv2.waitKey(0)
###  IMG_UP  ###
up_img = imutils.resize(up_img,width=200)
thresh = cv2.adaptiveThreshold(up_img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(9,3))
morph_img_threshold = thresh.copy()
cv2.morphologyEx(src=thresh, op=cv2.MORPH_CLOSE, kernel=kernel, dst=morph_img_threshold)
cv2.imshow('up', morph_img_threshold)
cv2.waitKey(0)
bitnot = cv2.bitwise_not(morph_img_threshold)
cv2.imshow('up', bitnot)
cv2.waitKey(0)
kernel = np.ones((7,7),np.uint8)
dilation = cv2.dilate(bitnot,kernel,iterations = 2)
cv2.imshow('up', dilation)
cv2.waitKey(0)
new,contours_up, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours_up= sorted(contours_up, key = cv2.contourArea, reverse = True)[:30]
contours_up = sort_contours(contours_up, method="left-to-right")
screenCnt = None
Y_up_sbd = []
Y_up_made = []
for c in contours_up:
    x,y,w,h = cv2.boundingRect(c)
    print(y)
    if w/h < 2:
        #print(y)
        out_up = up_img[y:y+h,x:x+w]
        cv2.imshow('a',out_up)
        cv2.waitKey(0)
        cv2.rectangle (up_img, (x, y), (x + w, y + h), (0,255,0), 2)
        if x>120:
            Y_up_made.append(y)
        elif x < 120:
            Y_up_sbd.append(y)
# print(Y_up_made)
# print(Y_up_sbd)  
made = ""   
sbd = ""
for i in range(len(Y_up_made)):
    if Y_up_made[i]<20:
        temp = 0
    elif Y_up_made[i]>20 and Y_up_made[i]<40:
        temp = 1
    elif Y_up_made[i]>40 and Y_up_made[i]<60:
        temp = 2
    elif Y_up_made[i]>60 and Y_up_made[i]<90:
        temp = 3
    elif Y_up_made[i]>100 and Y_up_made[i]<120:
        temp = 4
    elif Y_up_made[i]>120 and Y_up_made[i]<150:
        temp = 5
    elif Y_up_made[i]>150 and Y_up_made[i]<180:
        temp = 6
    made = made + str(temp)
print("ma de",made)
for i in range(len(Y_up_sbd)):
    if Y_up_sbd[i]<30:
        temp = 0
    elif Y_up_sbd[i]>30 and Y_up_sbd[i]<60:
        temp = 1
    elif Y_up_sbd[i]>60 and Y_up_sbd[i]<90:
        temp = 2
    elif Y_up_sbd[i]>90 and Y_up_sbd[i]<125:
        temp = 3
    elif Y_up_sbd[i]>125 and Y_up_sbd[i]<165:
        temp = 4
    elif Y_up_sbd[i]>165 and Y_up_sbd[i]<210:
        temp = 5
    elif Y_up_sbd[i]>210 and Y_up_sbd[i]<240:
        temp = 6
    sbd = sbd + str(temp)
print("sbd", sbd)


# ###   DOWN_IMG   ###
# ###LEFT###
# X_left = []
# down_img_left = imutils.resize(down_img_left,width=200)
# thresh_left = cv2.adaptiveThreshold(down_img_left,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
#             cv2.THRESH_BINARY,11,2)
# cv2.imshow('left', thresh_left)
# cv2.waitKey(0)
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(9,3))
# morph_img_threshold_left = thresh_left.copy()
# cv2.morphologyEx(src=thresh_left, op=cv2.MORPH_CLOSE, kernel=kernel, dst=morph_img_threshold_left)
# cv2.imshow('left', morph_img_threshold_left)
# cv2.waitKey(0)
# bitnot_left = cv2.bitwise_not(morph_img_threshold_left)
# cv2.imshow('left', bitnot_left)
# cv2.waitKey(0)
# kernel = np.ones((7,7),np.uint8)
# dilation_left = cv2.dilate(bitnot_left,kernel,iterations = 2)
# cv2.imshow('left', dilation_left)
# cv2.waitKey(0)
# new,contours_left, hierarchy = cv2.findContours(dilation_left, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# contours_left= sorted(contours_left, key = cv2.contourArea, reverse = True)[:30]
# contours_left = sort_contours(contours_left, method="top-to-bottom")
# screenCnt = None
# for c in contours_left:
#     x,y,w,h = cv2.boundingRect(c)
#     if w/h < 2:
#         # out_left = down_img_left[y:y+h,x:x+w]
#         # cv2.imshow('a',out_left)
#         # cv2.waitKey(0)
#         X_left.append(x)
#         cv2.rectangle (down_img_left, (x, y), (x + w, y + h), (0,255,0), 2)
# #print(X_left)
# cv2.imshow('left',down_img_left)
# cv2.waitKey(0)
# # for i in range(len(X_left)):
# #     if X_left[i]<50:
# #         print(i+1, "A")
# #     elif X_left[i]>50 and X_left[i]<100:
# #         print(i+1, "B")
# #     elif X_left[i]>100 and X_left[i]<150:
# #         print(i+1, "C")
# #     elif X_left[i]>150:
# #         print(i+1, "D")



# ###RIGHT###
# X_right = []
# down_img_right = imutils.resize(down_img_right,width=200)
# thresh_right = cv2.adaptiveThreshold(down_img_right,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
#             cv2.THRESH_BINARY,11,2)
# # cv2.imshow('right', thresh_right)
# # cv2.waitKey(0)
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(9,3))
# morph_img_threshold_right = thresh_right.copy()
# cv2.morphologyEx(src=thresh_right, op=cv2.MORPH_CLOSE, kernel=kernel, dst=morph_img_threshold_right)
# # cv2.imshow('right', morph_img_threshold_right)
# # cv2.waitKey(0)
# bitnot_right = cv2.bitwise_not(morph_img_threshold_right)
# # cv2.imshow('right', bitnot_right)
# # cv2.waitKey(0)
# kernel = np.ones((7,7),np.uint8)
# dilation_right = cv2.dilate(bitnot_right,kernel,iterations = 2)
# # cv2.imshow('right', dilation_right)
# # cv2.waitKey(0)
# new,contours_right, hierarchy = cv2.findContours(dilation_right, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# contours_right= sorted(contours_right, key = cv2.contourArea, reverse = True)[:30]
# contours_right = sort_contours(contours_right, method="top-to-bottom")
# screenCnt = None
# for c in contours_right:
#     x,y,w,h = cv2.boundingRect(c)
#     if w/h < 2:
#         X_right.append(x)
#         cv2.rectangle (down_img_right, (x, y), (x + w, y + h), (0,255,0), 2)
# cv2.imshow('right',down_img_right)
# cv2.waitKey(0)
# # print(X_right)
# KQ = X_left+X_right
# #print(KQ)
# DA = []
# for i in range(len(KQ)):
#     if KQ[i]<50:
#         print(i+1, "A")
#         DA.append("A")
#     elif KQ[i]>50 and KQ[i]<100:
#         print(i+1, "B")
#         DA.append("B")
#     elif KQ[i]>100 and KQ[i]<150:
#         print(i+1, "C")
#         DA.append("C")
#     elif KQ[i]>150:
#         print(i+1, "D")
#         DA.append("D")
# #print(DA)
# stt = []
# for i in range(1,51):
#     stt.append(i)
# print(stt)
# b = time.time()- a
# print(b)
# # # export = {'Sothutu':stt,
# # #             'DapAn':DA
# # #         }

# # # df = DataFrame(export, columns= ['Sothutu', 'DapAn'])
# # # print(df)
# # # datatoexcel = pd.ExcelWriter("fromPython.xlsx",engine="xlsxwriter")
# # # df.to_excel(datatoexcel,sheet_name="Sheet1")
# # # datatoexcel.save()

