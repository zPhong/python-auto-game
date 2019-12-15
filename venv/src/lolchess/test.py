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
exit_btn = [[88,51,67],[162,207,230]]

def check_white_px_in_rect(image,rect,limit = 1,name='B'):
    count = cv2.countNonZero(image[rect[1]:rect[1] + rect[3],rect[0]:rect[0] + rect[2]])
    cv2.imshow(name,image[rect[1]:rect[1] + rect[3],rect[0]:rect[0] + rect[2]])
    cv2.imwrite("images/exit-btn.png",image[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]])
    print(count/(rect[2]*rect[3]))
    if count > (rect[2]*rect[3])*0.025 and count < rect[2]*rect[3]*limit: #~ 33%
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




time.sleep(5)

isJoinGame = False
isPressStart = False

#img = cv2.imread('images/loss-all-hp.png', 1)
img = cv2.imread('images/loss-all-hp.png', 1)
img_2 = cv2.imread('images/landing.png',1)


res = cv2.inRange(img,  np.array(exit_btn[0])  , np.array(exit_btn[1]))
res2 =  cv2.inRange(img_2,  np.array(start_btn[0])  , np.array(start_btn[1]))
cv2.imshow('2',img_2[626:626 + 37,530:530 + 138])
check_white_px_in_rect(res,[510,362,161,36],0.04,'A')
# check_white_px_in_rect(res2,[530, 626, 138, 37])

# print(isHaveGame)
# if isHaveGame == True:
#     print('done')
# if check_white_px_in_rect(cv2.inRange(img,  np.array(avatar[0])  , np.array(avatar[1])),[570,232,48,38]) == False:
#     time.sleep(10)
#     isJoinGame = True
#

cv2.waitKey(0)
cv2.destroyAllWindows()