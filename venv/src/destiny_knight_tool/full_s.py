import copy
import os
import time
import win32api
import win32con
import cv2
import numpy as np
from PIL import ImageGrab

stop = False
list_color = [
	([17, 15, 120], [50, 56, 250] , '1'), #red
    ([120, 31, 4], [220, 88, 50], '2'),   #blue
    ([150, 33, 129], [245, 86, 150],'3'), #purple
    ([0,200, 41], [152, 222, 238], '4')   #green
]

rangesq = [1,2,3,4]

row , col = 7,12 #row,col
try_hard = 0

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

def click(x,y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def click_4S(mini, minj, maxi, maxj):
    # mini = minj = 0
    # maxi = 6
    # maxj = 11
    click(343 + 55 * (minj), 268 + 55 * (mini))
    time.sleep(0.3)

    click(343 + 55 * (maxj), 268 + 55 * (mini))
    time.sleep(0.3)

    click(343 + 55 * (maxj), 268 + 55 * (maxi))
    time.sleep(0.3)

    click(343 + 55 * (minj), 268 + 55 * (maxi))
    time.sleep(0.3)

top_left = [
    [0,0],[0,1],[1,0],[1,1]
]

bottom_right =[
    [6,11],[5,11],[6,10],[5,10]
]
def find_max_square():
    for (mini, minj) in top_left:
        for (maxi, maxj) in bottom_right:
            if not (mini == 1 and minj==1 and maxi == 5 and maxj == 10):
                if (matrix[mini][minj]==matrix[maxi][maxj] and
                    matrix[mini][minj] == matrix[mini, maxj] and
                    matrix[mini][minj] == matrix[maxi][minj]):
                    if ((maxj-minj == 11 or maxi-mini==6)
                        and (maxj-minj>9) and (maxi-mini>4)):
                        click_4S(mini, minj, maxi, maxj)
                        time.sleep(1)
                        return True


for i in range(4,0,-1):
    print(i)
    time.sleep(1)


while True:
    #click_4S(0,0,0,0)
    #time.sleep(1)

    matrix = np.zeros((row, col))

    scr = ImageGrab.grab(bbox=(268, 131, 865, 477))  # x, y, w, h
    img_np = np.array(scr)
    img_np = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

    # img_np = cv2.imread('images/11.png', 1)
    frame = img_np
    frame = cv2.resize(frame,(400,300))
    cv2.imshow("frame", frame)

    for (under, top, type) in list_color:
        res = copy.copy(img_np)
        res = cv2.inRange(res, np.array(under), np.array(top))
        #cv2.imshow('res', res)
        check_color_element(res, type)

    if (matrix[0][0] in rangesq):

        stop=True
        if try_hard < 0:
            try_hard += 1

            if (matrix[0][0]==matrix[0][11] and matrix[0][0]==matrix[6][0]
                and matrix[0][0]==matrix[6][11]):
                click_4S(0,0,6,11)
                time.sleep(3)

            click(343 + 55 * 11 + 15, 190)
            time.sleep(0.33)
            click(343 + 55 * 3, 268 + 55 * 3)
            time.sleep(0.1)
        else:
            if find_max_square():
                try_hard=0

            click(343 + 55*11 + 15, 190)
            time.sleep(0.33)
            click(343 + 55*3, 268 + 55* 3)
            time.sleep(0.1)
    else:
        if (stop==True):
            time.sleep(0.3)
            click(343 + 55 * 11 + 15, 190)
            time.sleep(0.3)
            stop=False
            click(343 + 55 * 3, 268 + 55 * 3)
            time.sleep(0.7)


    if cv2.waitKey(1) == 27:
        break