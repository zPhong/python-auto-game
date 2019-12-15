import cv2
import numpy as np

def recolor(src,maincolor,targetcolor):
    h, w, bpp = np.shape(src)
    for py in range(0, h):
        for px in range(0, w):
            subcolor = src[py][px] - maincolor
            src[py][px] = addcolor(subcolor, targetcolor)
    return src

def addcolor(subcolor, targetcolor):
    result = subcolor + targetcolor
    for i in list(range(0,2)):
        if result[i] < 0:
            result[i] = 0
        if result[i] > 255:
            result[i] = 255
    return result


#
# image = cv2.imread('images/model2.jpg')
# cv2.imshow('a',recolor(image ,np.array([96,126,197]) , np.array([215, 208 ,231])))
#
# cv2.waitKey(0)