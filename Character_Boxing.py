
import numpy as np
import cv2
from keras.preprocessing.image import img_to_array
from imutils import contours
import imutils

import os
import glob

# clearing out the images for boxing
files = glob.glob('./images/*')
for f in files:
    os.remove(f)

# getting contour precendence for sorting the contours
def contour_rank(contour, cols):
    tolerance_factor = 50
    origin = cv2.boundingRect(contour)
    #print("origin" +str(origin))
    return ((origin[1] // tolerance_factor) * tolerance_factor) * cols + origin[0]

# current image's index
f = open("current_image.txt", "r")
n = int(f.read())

# reading the mathematical expression
image = cv2.imread("./MathExpressions/exp" + str(n) + ".png")
image = cv2.copyMakeBorder(image,50,50,50,50,cv2.BORDER_CONSTANT,value=[255,255,255])
orig = image.copy()

# keeping parameters of images
keepy = []
keepx = []
keeph = []
keepw = []

# grayscale, thresholding
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# find contours and sort
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
cnts.sort(key=lambda x: contour_rank(x, thresh.shape[0]))

# find x values
for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    y = y - 20
    x = x - 20
    w = w + 50
    h = h + 50
    if x not in keepx:
        keepx.append(x)
keepx.sort()

# adding as many values as in keepx
for i in range(0,len(keepx)):
    keepy.append(i)
    keeph.append(i)
    keepw.append(i)

# changing the y, h, w values to the correct ordered ones
for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    y = y - 20
    x = x - 20
    w = w + 50
    h = h + 50
    for i in range(0,len(keepx)):
        if(keepx[i]==x):
            keepy[i] = y
            keeph[i] = h
            keepw[i] = w


previous = 0
previoush = 0
# prev is true if the element is on level 2
prev = False
count = 0

for i in range(0, len(keepx)):
    # adding bounding box
    cv2.rectangle(image, (keepx[i], keepy[i]), (keepx[i] + keepw[i], keepy[i] + keeph[i]), (50, 255, 20), 2)
    ROI = orig[keepy[i]:keepy[i] + keeph[i], keepx[i]:keepx[i] + keepw[i]]
    if (i != 0):
        # if the previous character was in level 2
        if (prev == True):
            # if the last element is on level 2
            if(i == len(keepx) - 1):
                cv2.imwrite('./images/ROIpowerEND_{}.png'.format(i), ROI)
                prev = False
            # if this is the last element on level 2
            elif((keepy[i-1]+keeph[i-1]/2) < keepy[i]):
                cv2.imwrite('./images/ROIpower_{}.png'.format(i), ROI)
                prev = False
            # if this is on level 2
            else:
                cv2.imwrite('./images/ROIpow_{}.png'.format(i), ROI)
                prev = True
        # if this is element on level 1
        else:
            if ((keepy[i]+keeph[i]/17)- keepy[i-1] < 0):
                # if the character is on level 2
                if(keeph[i-1]>keeph[i]):
                    print(keepy[i]+keeph[i]/3)
                    print(keepy[i-1])
                    # if only this element is on level 2
                    if (keepy[i]+keeph[i]/3) < (keepy[i-1]):
                        cv2.imwrite('./images/powerSLASH_{}.png'.format(i), ROI)
                        prev = False
                    # if this element is only level 2 and there is more
                    else:
                        cv2.imwrite('./images/power_{}.png'.format(i), ROI)
                        prev = True
                # if the character is not on level 2
                else:
                    cv2.imwrite('./images/ROI_{}.png'.format(i), ROI)
                    prev = False
            # if the character is on level 1
            else:
                    cv2.imwrite('./images/ROI_{}.png'.format(i), ROI)
                    prev = False
    # this is for the first element
    else:
        cv2.imwrite('./images/ROI_{}.png'.format(i), ROI)
        prev = False

    previous = keepy[i]
    previoush = keeph[i]
    count += 1
    i += 1

# keeping count of how many characters are in the expression
open('count_images.txt', 'w').close()
f = open("count_images.txt", "a")
f.write(str(count))
f.close()

# keeping the mathematical expression with bounding boxes
cv2.imwrite('imageboxing.png', image)
cv2.waitKey()

