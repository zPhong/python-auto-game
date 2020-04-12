import copy
import os
import time
import win32api
import win32con
import cv2
import numpy as np
from PIL import ImageGrab

play_btn = [[200,0,0],[250,250,255]]
start_btn = [[30,35,30],[50,50,50]]
avatar = [[0,0,94],[42,21,250]]
exit_btn = [[82,69,8],[186,120,12]]

def check_white_px_in_rect(image,rect,limit = 1,name='B'):
    count = cv2.countNonZero(image[rect[1]:rect[1] + rect[3],rect[0]:rect[0] + rect[2]])
    cv2.imshow(name,image[rect[1]:rect[1] + rect[3],rect[0]:rect[0] + rect[2]])
    #cv2.imwrite("images/loss-all-hp.png",image[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]])
    print(count/(rect[2]*rect[3]))
    if count > (rect[2]*rect[3])*0.25 and count < rect[2]*rect[3]*limit: #~ 33%
        print("1")
        return 1

    print(count,(rect[2]*rect[3])*0.25 ,rect[2]*rect[3]*limit)
    print('0')
    return 0



def click(x,y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

def check_is_full_black_px(image,rect):
    count = cv2.countNonZero(image[rect[1]:rect[1] + rect[3],rect[0]:rect[0] + rect[2]])

    if count > 0:
        return 0

    return 1

def sellChampion():
    win32api.SetCursorPos((308, 543))
    time.sleep(1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 308, 543, 0, 0)
    time.sleep(1)
    win32api.SetCursorPos((450, 743))
    time.sleep(1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,450, 743, 0, 0)

#550,10,27,12
def compareImage(image):
    i1 = cv2.imread('images\\round-end.png',1)
    i2 = image[10:22,550:577]
    cv2.imwrite('images\\round-end.png',i2)
    cv2.imshow('1',i1);
    cv2.imshow('2',i2);
    difference = cv2.subtract(i1, i2)
    b, g, r = cv2.split(difference)
    if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
        return True;
    return False

def clickSurrender():
    click(1355,630)
    time.sleep(5)
    click(490,695)
    time.sleep(5)
    click(610,430)
    time.sleep(10)

def isAgain():
    i1 = cv2.imread('images\\btn-again.png',1)
    i2 = cv2.imread('images\\again.png')[635:650,570:630]
    cv2.imshow('1', i1);
    cv2.imshow('2', i2);
    cv2.imwrite('images\\btn-again.png',i2)
    difference = cv2.subtract(i1, i2)
    b, g, r = cv2.split(difference)
    if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
        return True;
    return False

print(isAgain())

cv2.waitKey(0)
cv2.destroyAllWindows()