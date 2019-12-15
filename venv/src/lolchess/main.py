import copy
import os
import time
import win32api
import win32con
import cv2
import numpy as np
from PIL import ImageGrab

index = 1;
count = 0;

play_btn = [[200,0,0],[250,250,255]]
avatar = [[0,0,94],[42,21,250]]
exit_btn = [[200,0,0],[250,250,255]]
start_btn = [[30,35,30],[50,50,50]]

base_resolution = [1366,768]

desktop_resolution = [win32api.GetSystemMetrics(0),win32api.GetSystemMetrics(1)]

print(desktop_resolution)

aspectRatio = [1,1]
addtionPixel = [0,0]#[(base_resolution[0] - desktop_resolution[0])/2, (base_resolution[1] - desktop_resolution[1])/2]
print(addtionPixel)

cv2.namedWindow('Check')
cv2.moveWindow('Check', 0,0)


font                   = cv2.FONT_HERSHEY_SIMPLEX
fontScale              = 0.35
lineType               = 2

# Create a black image
img = np.zeros((500,100,3), np.uint8)
cv2.putText(img, '0',
                (20, 480),
                font,
                fontScale,
                (255,255,255),
                lineType)

img_exit_btn = cv2.imread('images\exit-btn',1)

def check_white_px_in_rect(image,_rect,limit = 1,isScale = True):
    rect = _rect
    if isScale == True:
        rect = [int(_rect[0]*aspectRatio[0] + addtionPixel[0]),
                int(_rect[1]*aspectRatio[1] + addtionPixel[1]),
                int(_rect[2]*aspectRatio[0]),
                int(_rect[3]*aspectRatio[1])]
    count = cv2.countNonZero(image[rect[1]:rect[1] + rect[3],rect[0]:rect[0] + rect[2]])
    cv2.imshow('Check',image[rect[1]:rect[1] + rect[3],rect[0]:rect[0] + rect[2]])
    if count > (rect[2]*rect[3])*0.025 and count < rect[2]*rect[3]*limit: #~ 33%
        return 1

    return 0

def detectExit_btn(image, _rect, limit = 1, isScale = True):
    rect = _rect
    if isScale == True:
        rect = [int(_rect[0] * aspectRatio[0] + addtionPixel[0]),
    int(_rect[1] * aspectRatio[1] + addtionPixel[1]),
    int(_rect[2] * aspectRatio[0]),
    int(_rect[3] * aspectRatio[1])]
    count = cv2.countNonZero(image[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]])
    cv2.imshow('Check', image[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]])
    if count > (rect[2] * rect[3]) * 0.03 \
            and count < rect[2] * rect[3] * limit:
            #and np.array_equal(np.array(img_exit_btn),np.array(image[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]])):  # ~ 33%
        return 1
    return 0

def check_is_full_black_px(image,_rect,isScale = True):
    rect = _rect
    if isScale == True:
        rect = [int(_rect[0] * aspectRatio[0] + addtionPixel[0]),
                int(_rect[1] * aspectRatio[1] + addtionPixel[1]),
                int(_rect[2] * aspectRatio[0]),
                int(_rect[3] * aspectRatio[1])]
    count = cv2.countNonZero(image[rect[1]:rect[1] + rect[3],rect[0]:rect[0] + rect[2]])

    if count > 0:
        return 0

    return 1

def click(_x,_y,isScale = False):
    x = _x
    y = _y
    if isScale == True:
        x = int(_x * aspectRatio[0] + addtionPixel[0])
        y = int(_y * aspectRatio[1] + addtionPixel[1])


    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

def sellChampion():
    try:
        win32api.SetCursorPos((int(308*aspectRatio[0] + addtionPixel[0]),
                               int(543*aspectRatio[1] + addtionPixel[1])))
        time.sleep(1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,
                             int(308*aspectRatio[0] + addtionPixel[0]),
                             int(543*aspectRatio[1] + addtionPixel[1]), 0, 0)
        time.sleep(1)
        win32api.SetCursorPos((int(450*aspectRatio[0] + addtionPixel[0])
                               ,int(743*aspectRatio[1] + addtionPixel[1])))
        time.sleep(1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,
                             int(450*aspectRatio[0] + addtionPixel[0]),
                             int(743*aspectRatio[1] + addtionPixel[1]), 0, 0)
    except NameError:
        print(NameError)
def reset(count):
    global img
    img = np.zeros((500,100, 3), np.uint8)
    cv2.putText(img, 'total : ' + str(count),
                (20, 480),
                font,
                fontScale,
                (255,255,255),
                lineType)

def logger(str, index, color):
    cv2.putText(img, str,
                (20,30*index),
                font,
                fontScale,
                color,
                lineType)

    cv2.imshow('Logger',img)




time.sleep(5)

isJoinGame = False
isPressStart = False
isFinishGame = False

exitBtnDetectedCount = 0


while True:
    scr = ImageGrab.grab(bbox=(0,0,1366,768))
    img_np = np.array(scr)
    img_np = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
    res = cv2.inRange(img_np,  np.array(play_btn[0])  , np.array(play_btn[1]))
    if isPressStart == False:
        isShowAgainBtn = check_white_px_in_rect(cv2.inRange(img_np, np.array(start_btn[0]), np.array(start_btn[1])),[530, 626, 138, 37])
        if isShowAgainBtn == True:
            click(596, 641)
            click(596, 641)
            logger('Press play',index ,(200,0,100))
            index += 1
            isPressStart = True

    # step 1:find game
    if isJoinGame == False:
        isHaveGame = check_white_px_in_rect(res,[593,512,176,60])
        if isHaveGame == True:
            click(680, 550)
            logger('Press ok',index,(200,1000, 0))


        if check_is_full_black_px(cv2.cvtColor(img_np,cv2.COLOR_RGB2GRAY), [400, 222, 300, 300]) == True:
            index += 1
            logger('Join game',index,(200,1000, 0))
            index += 1
            isJoinGame = True

    else:
        if isFinishGame == False:
            isShowExit = detectExit_btn(cv2.inRange(img_np,  np.array(exit_btn[0])  , np.array(exit_btn[1])),[510,362,161,36],0.035)
            if isShowExit == True:
                exitBtnDetectedCount += 1
                if exitBtnDetectedCount < 6:
                    time.sleep(7)
                if exitBtnDetectedCount == 6:
                    print('exit')
                    click(600,380)
                    time.sleep(2)
                    click(600,380)
                    time.sleep(5)
                    index += 1
                    logger('Press-exit',index, (100, 24, 10))
                    index += 1
                    isFinishGame = True
                    time.sleep(10)
            else:
                exitBtnDetectedCount = 0
                logger('Sell-champ',index, (100, 24, 10))
                sellChampion()
                time.sleep(5)
        else:
            isShowAgainBtn = check_white_px_in_rect(cv2.inRange(img_np,np.array(start_btn[0]),np.array(start_btn[1])),[530, 626, 138, 37])
            if isShowAgainBtn == True:
                time.sleep(2)
                logger('Press play again',index, (50, 30, 170))
                click(596, 641)
                time.sleep(5)
                index += 1
                logger('Reseting...',index, (50, 30, 170))
                index = 1
                count += 1
                isJoinGame = False
                isPressStart = False
                isFinishGame = False
                exitBtnDetectedCount = 0
                reset(count)

    if cv2.waitKey(1) == 27:
        break
cv2.waitKey(0)
cv2.destroyAllWindows()