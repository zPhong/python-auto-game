import numpy as np
import cv2
import os
import time
import copy

from face_detect_landmark import get_landmarks
from face_detect_landmark import get_landmarks_pts
from face_detect_landmark import get_delaunay_array
from face_detect_landmark import draw_delaunay
from face_detect_landmark import draw_Contour
from face_detect_landmark import transformation_from_points
from face_detect_landmark import warp_im

from color_transfer import recolor
from affine_triangle import transform

model = cv2.imread('images/model4.jpg', 1)
user = cv2.imread('images/user.jpg', 1)

# user = cv2.resize(user,(600,800))
# model = cv2.resize(model,(600,800))

size = model.shape
userSize = user.shape
user = cv2.resize(user,(size[1],size[0]))
clone = copy.copy(user)
userPts, rectUser = get_landmarks(user, "User")
modelPts, rectModel = get_landmarks(model, "Model")

divModel = get_delaunay_array(model,modelPts)
divUser  = get_delaunay_array(user,modelPts)

# draw_Contour(model,modelPts)

# result = transform(model,user,divModel,modelPts,userPts)
#
# result = cv2.resize(result,(userSize[1],userSize[0]));

#draw_delaunay(model, divModel, (255, 255, 255))
cv2.imshow('User',user)
cv2.imshow('Model',model)

result = transform(model,user,divModel,modelPts,userPts)

(x,y) = (userPts[30][0,0],userPts[30][0,1])
(mx,my) = (modelPts[30][0,0],modelPts[30][0,1])
print(result[y][x])
print(clone[y][x])

result = recolor(result,result[y][x],clone[y][x])
cv2.imshow('Result',result)

result = cv2.resize(result,(userSize[1],userSize[0]));

cv2.waitKey(0)

cv2.destroyAllWindows()
