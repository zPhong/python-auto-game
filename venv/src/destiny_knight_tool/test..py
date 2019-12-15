import copy
import os
import time
import win32api
import win32con
import cv2
import numpy as np
from PIL import ImageGrab
from mouseControl import getPosition
list_color = [
	([17, 15, 120], [50, 56, 250] , '1'), #red
    ([120, 31, 4], [220, 88, 50], '2'),   #blue
    ([150, 33, 129], [245, 86, 150],'3'), #purple
    ([0,200, 41], [152, 222, 238], '4')   #green
]

row , col = 7,12 #row,col

matrix = np.zeros((row, col))

allowClick = False

screenRect = [268, 131, 865, 477]

miniRect = [(int)((screenRect[2]-screenRect[0])/12),(int)((screenRect[3]-screenRect[1])/12)]




def check_white_px_in_rect(image,rect):
    count = cv2.countNonZero(image[rect[1]:rect[1] + rect[3],rect[0]:rect[0] + rect[2]])

    if count > (rect[2]*rect[3])/30: #~ 33%
        return 1

    return 0

def check_color_element(image , type):
    h , w = np.shape(image)
    h   = (int)(h / row);
    w = (int)(w / col);

    for x in range(col):
        for y in range(row):
            if check_white_px_in_rect(image,[x*w,y*h,w,h]) == 1:
                matrix[y,x] = type

def print_result_to_console(mini, minj, maxi, maxj):
    result = \
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    if matrix[mini][minj] == 1:
        result[mini][minj] = 'D'
        result[maxi][maxj] = 'D'
        result[mini][maxj] = 'D'
        result[maxi][minj] = 'D'
    else:
        if matrix[mini][minj] == 2:
            result[mini][minj] = 'B'
            result[maxi][maxj] = 'B'
            result[mini][maxj] = 'B'
            result[maxi][minj] = 'B'
        else:
            if matrix[mini][minj] == 3:
                result[mini][minj] = 'T'
                result[maxi][maxj] = 'T'
                result[mini][maxj] = 'T'
                result[maxi][minj] = 'T'
            else:
                if matrix[mini][minj] == 4:
                    result[mini][minj] = 'X'
                    result[maxi][maxj] = 'X'
                    result[mini][maxj] = 'X'
                    result[maxi][minj] = 'X'

    print('{},{},{},{}'.format(mini,minj,maxi,maxj))
    for i in range(row):
        for j in range(col):
            print(result[i][j], ' ', end='')
        print()
    print('----------------------------------')

def click(x,y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

def click_result(mini, minj, maxi, maxj):
    click((int)(screenRect[0] + miniRect[0]/2 + miniRect[0] * (minj)), (int)(screenRect[1] + miniRect[1]/2 + miniRect[1] * (mini)))
    time.sleep(0.3)

    click((int)(screenRect[0] + miniRect[0]/2 + miniRect[0] * (maxj)), (int)(screenRect[1] + miniRect[1]/2 + miniRect[1] * (mini)))
    time.sleep(0.3)

    click((int)(screenRect[0] + miniRect[0]/2 + miniRect[0] * (maxj)), (int)(screenRect[1] + miniRect[1]/2 + miniRect[1] * (maxi)))
    time.sleep(0.3)

    click((int)(screenRect[0] + miniRect[0]/2 + miniRect[0] * (minj)), (int)(screenRect[1] + miniRect[1]/2 + miniRect[1] * (maxi)))
    time.sleep(0.3)

def render_rect(image,mini,minj,maxi,maxj):
    cv2.rectangle(image
                  , (miniRect[0] * minj, miniRect[1] * mini)
                  , (miniRect[0] + miniRect[0] * minj, miniRect[1] + miniRect[1] * mini)
                  , (255, 25, 25), 1)
    cv2.rectangle(frame
                  , (miniRect[0] * maxj, miniRect[1] * mini)
                  , (miniRect[0] + miniRect[0] * maxj, miniRect[1] + miniRect[1] * mini)
                  , (255, 25, 25), 1)

    cv2.rectangle(frame
                  , (miniRect[0] * minj, miniRect[1] * maxi)
                  , (miniRect[0] + miniRect[0] * minj, miniRect[1] + miniRect[1] * maxi)
                  , (255, 25, 25), 1)

    cv2.rectangle(frame
                  , (miniRect[0] * maxj, miniRect[1] * maxi)
                  , (miniRect[0] + miniRect[0] * maxj, miniRect[1] + miniRect[1] * maxi)
                  , (255, 25, 25), 1)


print('start')
temp = getPosition()
screenRect[0] = temp[0]
screenRect[1] = temp[1]

print('end')
temp = getPosition()
screenRect[2] = temp[0]
screenRect[3] = temp[1]
print("generate Zone :")

miniRect = [(int)((screenRect[2]-screenRect[0])/12),(int)((screenRect[3]-screenRect[1])/7)]



while True:
    scr = ImageGrab.grab(bbox=(screenRect[0], screenRect[1], screenRect[2], screenRect[3]))  # x, y, w, h
    img_np = np.array(scr)
    img_np = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

    # img_np = cv2.imread('images/11.png', 1)
    frame = img_np


    for (under, top, type) in list_color:
        res = copy.copy(img_np)
        res = cv2.inRange(res, np.array(under), np.array(top))
        #cv2.imshow('res', res)
        check_color_element(res, type)

    #print(matrix)

    max = mini = minj = maxi = maxj = 0

    for i in range(row - 1):
        for j in range(col - 1):
            for x in range(row-1,i, -1):
                for y in range(col-1, j, -1 ):
                    #print(i,' ',j,' ',x,' ',y,' ',matrix[i][j],' ',matrix[x][y])
                    if (matrix[x][y]==matrix[i][j] and matrix[i][y]==matrix[x][y]
                                and matrix[x][y]==matrix[x][j]):
                        val = (x-i)*(y-j)
                        if val>max:
                            max = val; mini=i; minj=j; maxi=x; maxj=y

    render_rect(frame,mini,minj,maxi,maxj)
    #frame = cv2.resize(frame,(400,300))
    cv2.imshow("frame", frame)

    print_result_to_console(mini, minj, maxi, maxj)


    click_result(mini, minj, maxi, maxj)

    time.sleep(1)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
