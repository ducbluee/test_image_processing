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

def read(img):
    img = imutils.resize(img,width=200)
    thresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                cv2.THRESH_BINARY,11,2)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(9,3))
    morph = thresh.copy()
    cv2.morphologyEx(src=thresh, op=cv2.MORPH_CLOSE, kernel=kernel, dst=morph)
    bitnot = cv2.bitwise_not(morph)
    kernel = np.ones((7,7),np.uint8)
    dilation = cv2.dilate(bitnot,kernel,iterations = 2)
    return dilation

def ex_ct(dilation):
    X = []
    new,contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours= sorted(contours, key = cv2.contourArea, reverse = True)[:30]
    contours = sort_contours(contours, method="top-to-bottom")
    screenCnt = None
    for c in contours:
        x,y,w,h = cv2.boundingRect(c)
        if w/h < 2:
            X.append(x)
    return X

def ex_ct_up(dilation):
    new,contours, hierarchy = cv2.findContours(dila_up, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours= sorted(contours, key = cv2.contourArea, reverse = True)[:30]
    contours = sort_contours(contours, method="left-to-right")
    screenCnt = None
    Y_up_sbd = []
    Y_up_made = []
    for c in contours:
        x,y,w,h = cv2.boundingRect(c)
        if w/h < 2:
            if x>120:
                Y_up_made.append(y)
            elif x < 120:
                Y_up_sbd.append(y)
    return Y_up_sbd, Y_up_made

def vote(Y):
    string = ""
    for i in range(len(Y)):
        if Y[i]<20:
            temp = 0
        elif Y[i]>20 and Y[i]<40:
            temp = 1
        elif Y[i]>40 and Y[i]<60:
            temp = 2
        elif Y[i]>60 and Y[i]<90:
            temp = 3
        elif Y[i]>100 and Y[i]<120:
            temp = 4
        elif Y[i]>120 and Y[i]<150:
            temp = 5
        elif Y[i]>150 and Y[i]<180:
            temp = 6

        string = string + str(temp)
    return string

####

img = cv2.imread('t1.png')
# cv2.imshow('img', img)
# cv2.waitKey(0)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2.imshow('1', gray)
# cv2.waitKey(0)


im_width = gray.shape[1]
im_height = gray.shape[0]

up_img = gray[int(0.12*im_height):int(0.34*im_height), int(0.68*im_width):int(0.92*im_width)]
# cv2.imshow('2',up_img)
# cv2.waitKey(0)
down_img_right = gray[int(0.41*im_height):int(0.92*im_height), int(0.6*im_width):int(0.8*im_width)]
# cv2.imshow('2',down_img_right)
# cv2.waitKey(0)
down_img_left = gray[int(0.41*im_height):int(0.92*im_height), int(0.18*im_width):int(0.38*im_width)]
# cv2.imshow('2',down_img_left)
# cv2.waitKey(0)

###
dila_up = read(up_img)
dila_left = read(down_img_left)
dila_right = read(down_img_right)
X_left = ex_ct(dila_left)
X_right = ex_ct(dila_right)
Y_sbd, Y_ma = ex_ct_up(dila_up)

sbd = vote(Y_sbd)
print(sbd)
made = vote(Y_ma)
print(made)
KQ = X_left+X_right
for i in range(len(KQ)):
    if KQ[i]<50:
        print(i+1, "A")
    elif KQ[i]>50 and KQ[i]<100:
        print(i+1, "B")
    elif KQ[i]>100 and KQ[i]<150:
        print(i+1, "C")
    elif KQ[i]>150:
        print(i+1, "D")

b = time.time() - a
print(b)