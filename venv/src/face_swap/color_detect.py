import cv2
import numpy as np
import copy

list_color = [
	([17, 15, 120], [50, 56, 250] , '1'), #red
    ([120, 31, 4], [220, 88, 50], '2'),   #blue
    ([150, 33, 129], [245, 86, 150],'3'), #purple
    ([0,200, 41], [152, 222, 238], '4')   #green
]

row , col = 7,12 #row,col

matrix = np.zeros((row, col))

def check_white_px_in_rect(image,rect):
    count = cv2.countNonZero(image[rect[1]:rect[1] + rect[3],rect[0]:rect[0] + rect[2]])

    if count > (rect[2]*rect[3])/30: #~ 33%
        return 1

    return 0


def check_color_element(image , type):
    h , w = np.shape(image)
    h = (int)(h / row);
    w = (int)(w / col);

    for x in range(col):
        for y in range(row):
            if check_white_px_in_rect(image,[x*w,y*h,w,h]) == 1:
                matrix[y,x] = type


img = cv2.imread('images/diamond3.png',1);

cv2.imshow('test',img);




for(under,top , type) in list_color:
    res = copy.copy(img);

    res = cv2.inRange(res,np.array(under),np.array(top));

    cv2.imshow('res',res);
    check_color_element(res, type)

    cv2.waitKey(0)


print(matrix)
cv2.waitKey(0)

cv2.destroyAllWindows()