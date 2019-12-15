import numpy as np
import cv2

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



def reset(count):
    img = np.zeros((500,100, 3), np.uint8)
    cv2.putText(img, str(count),
                (20, 500),
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