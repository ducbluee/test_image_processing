import numpy as np
import argparse
import imutils
import cv2


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

def process(img):
        img_hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # lower mask (0-10)
        lower_red = np.array([0,50,50])
        upper_red = np.array([10,255,255])
        mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

        # upper mask (170-180)
        lower_red = np.array([170,50,50])
        upper_red = np.array([180,255,255])
        mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

        # join my masks
        mask = mask0+mask1

        # set my output img to zero everywhere except my mask
        output_img = img.copy()
        output_img[np.where(mask==0)] = 0

        # or your HSV image, which I *believe* is what you want
        output_hsv = img_hsv.copy()
        output_hsv[np.where(mask==0)] = 0

        canny = cv2.Canny(output_hsv,100,200)
        return canny

def find(img):
        new,contour, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contour= sorted(contour, key = cv2.contourArea, reverse = True)[:50]
        contour = sort_contours(contour, method="top-to-bottom")
        return contour

def convex(contour):
        for cnt in contours:
                hull = cv2.convexHull(cnt)
                cv2.drawContours(canny, [cnt], -1, 255, -1)
                cv2.drawContours(canny, [hull], -1, 255, -1)
        return canny

img = cv2.imread('2.png')
img1 = cv2.imread('anh1.png')
img1 = imutils.resize(img1,width=676)
# cv2.imshow('img',img)
# cv2.waitKey(0)

canny = process(img)

new,contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours= sorted(contours, key = cv2.contourArea, reverse = True)[:33]
screenCnt = None
canny = convex(contours)
height, width, channels = img1.shape

new,contours1, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours1= sorted(contours1, key = cv2.contourArea, reverse = True)[:9]
contours1 = sort_contours(contours1, method="top-to-bottom")
array = []

for c in contours1:
        x,y,w,h = cv2.boundingRect(c)
        cut = img[y:y+h,x:x+w]
        # cv2.imshow('img',cut)
        # cv2.waitKey(0)
        array.append(cut)
        #cv2.rectangle (img1, (x, y), (x + w, y + h), (0,255,0), 2)


for i in range(len(array)):
        if i==0:
                canny = process(array[i])
                new,contours2, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                contours2= sorted(contours2, key = cv2.contourArea, reverse = True)[:50]
                contours2 = sort_contours(contours2, method="top-to-bottom")
                for c in contours2:
                        x,y,w,h = cv2.boundingRect(c)
                        if w*h > 4500 and w*h<9000:
                                a = array[i][y:y+h,x:x+w]
                                cv2.rectangle (array[i], (x, y), (x + w, y + h), (0,255,0), 2)
                                cv2.imshow('img',a)
                                cv2.waitKey(0)
                cv2.imshow('img',array[i])
                cv2.waitKey(0)
        elif i==1:
                canny = process(array[i])
                new,contours2, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                contours2= sorted(contours2, key = cv2.contourArea, reverse = True)[:25]
                contours2 = sort_contours(contours2, method="top-to-bottom")
                for c in contours2:
                        x,y,w,h = cv2.boundingRect(c)
                        if w*h > 1500 and w*h<4500:
                                a = array[i][y:y+h,x:x+w]
                                cv2.rectangle (array[i], (x, y), (x + w, y + h), (0,255,0), 2)
                                cv2.imshow('img',a)
                                cv2.waitKey(0)
                cv2.imshow('img',array[i])
                cv2.waitKey(0)
        elif i==2:
                canny = process(array[i])
                new,contours2, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                contours2= sorted(contours2, key = cv2.contourArea, reverse = True)[:18]
                contours2 = sort_contours(contours2, method="top-to-bottom")
                for c in contours2:
                        x,y,w,h = cv2.boundingRect(c)
                        if w*h > 1100 and w*h<1300:
                                a = array[i][y:y+h,x:x+w]
                                cv2.rectangle (array[i], (x, y), (x + w, y + h), (0,255,0), 2)
                                cv2.imshow('img',a)
                                cv2.waitKey(0)
                cv2.imshow('img',array[i])
                cv2.waitKey(0)
        elif i==3:
                canny = process(array[i])
                new,contours2, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                contours2= sorted(contours2, key = cv2.contourArea, reverse = True)[:70]
                contours2 = sort_contours(contours2, method="top-to-bottom")
                for c in contours2:
                        x,y,w,h = cv2.boundingRect(c)
                        if w*h > 650 and w*h<1700:
                                a = array[i][y:y+h,x:x+w]
                                cv2.rectangle (array[i], (x, y), (x + w, y + h), (0,255,0), 2)
                                cv2.imshow('img',a)
                                cv2.waitKey(0)
                cv2.imshow('img',array[i])
                cv2.waitKey(0)
        elif i==4:
                canny = process(array[i])
                new,contours2, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                contours2= sorted(contours2, key = cv2.contourArea, reverse = True)[:5]
                contours2 = sort_contours(contours2, method="top-to-bottom")
                for c in contours2:
                        x,y,w,h = cv2.boundingRect(c)
                        a = array[i][y:y+h,x:x+w]
                        cv2.rectangle (array[i], (x, y), (x + w, y + h), (0,255,0), 2)
                        cv2.imshow('img',a)
                        cv2.waitKey(0)
                cv2.imshow('img',array[i])
                cv2.waitKey(0)
        elif i==5:
                canny = process(array[i])
                new,contours2, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                contours2= sorted(contours2, key = cv2.contourArea, reverse = True)[:5]
                contours2 = sort_contours(contours2, method="top-to-bottom")
                for c in contours2:
                        x,y,w,h = cv2.boundingRect(c)
                        if w*h > 900 and w*h<1200:
                                a = array[i][y:y+h,x:x+w]
                                cv2.rectangle (array[i], (x, y), (x + w, y + h), (0,255,0), 2)
                                cv2.imshow('img',a)
                                cv2.waitKey(0)
                cv2.imshow('img',array[i])
                cv2.waitKey(0)
        elif i==6:
                canny = process(array[i])
                new,contours2, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                contours2= sorted(contours2, key = cv2.contourArea, reverse = True)[:30]
                contours2 = sort_contours(contours2, method="top-to-bottom")
                for c in contours2:
                        x,y,w,h = cv2.boundingRect(c)
                        if w*h > 900 and w*h<2000 and h/w>0.8:
                                a = array[i][y:y+h,x:x+w]
                                cv2.rectangle (array[i], (x, y), (x + w, y + h), (0,255,0), 2)
                                cv2.imshow('img',a)
                                cv2.waitKey(0)
                cv2.imshow('img',array[i])
                cv2.waitKey(0)
        elif i==7:
                canny = process(array[i])
                new,contours2, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                contours2= sorted(contours2, key = cv2.contourArea, reverse = True)[:20]
                contours2 = sort_contours(contours2, method="top-to-bottom")
                for c in contours2:
                        x,y,w,h = cv2.boundingRect(c)
                        if w*h > 900 and w*h<2000 and h/w>0.8:
                                a = array[i][y:y+h,x:x+w]
                                cv2.rectangle (array[i], (x, y), (x + w, y + h), (0,255,0), 2)
                                cv2.imshow('img',a)
                                cv2.waitKey(0)
                cv2.imshow('img',array[i])
                cv2.waitKey(0)
        elif i==8:
                canny = process(array[i])
                new,contours2, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                contours2= sorted(contours2, key = cv2.contourArea, reverse = True)[:30]
                contours2 = sort_contours(contours2, method="top-to-bottom")
                for c in contours2:
                        x,y,w,h = cv2.boundingRect(c)
                        if w*h > 4500 and w*h<9000:
                                a = array[i][y:y+h,x:x+w]
                                cv2.rectangle (array[i], (x, y), (x + w, y + h), (0,255,0), 2)
                                cv2.imshow('img',a)
                                cv2.waitKey(0)
                cv2.imshow('img',array[i])
                cv2.waitKey(0)

# cv2.imshow('img',img1)
# cv2.waitKey(0)

