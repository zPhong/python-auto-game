import cv2
import numpy as np
import copy
import time

RIGHT_EYE_POINTS = list(range(36, 42))
LEFT_EYE_POINTS = list(range(42, 48))
TOOTH_POINTS = list(range(60, 68))
NOSE_POINTS = list(range(27, 36))

#Region replace
TOP_LIP_POINTS = [48,49,50,51,52,53,54,60,61,62,63,65]
BOT_LIP_POINTS = [48,54,55,56,57,58,59,60,64,65,66,67]
EYE_REGION_POINTS = [0,16,17,18,19,20,21,22,23,24,25,26,27,36,37,38,39,42,43,44,45]

from face_detect_landmark import rect_contains

def list_contains_triangle(triangle,list):
    pt1 = [(int)(triangle[0]), (int)(triangle[1])]
    pt2 = [(int)(triangle[2]), (int)(triangle[3])]
    pt3 = [(int)(triangle[4]), (int)(triangle[5])]

    i = list_contains_point(pt1,list)*list_contains_point(pt2,list)*list_contains_point(pt3,list)
    return i

def list_contains_point(point,list):
    for p in list:
        if point == [p[0,0], p[0,1]]:
            return 1
    return 0

def transform(model, user, srcdiv , srcShape , desShape):

    #user = 255 * np.ones(model.shape, dtype=model.dtype)

    srcTList , desTList = get_listTriangle(model,srcdiv,srcShape , desShape)

    index = 0

    while index < srcTList.__len__():
        src = srcTList[index]
        des = desTList[index]
        # Find bounding box.
        r1 = cv2.boundingRect(src)
        r2 = cv2.boundingRect(des)

        # Offset points by left top corner of the
        # respective rectangles

        srcCropped = []
        desCropped = []

        for i in range(0, 3):
            srcCropped.append(((src[0][i][0] - r1[0]), (src[0][i][1] - r1[1])))
            desCropped.append(((des[0][i][0] - r2[0]), (des[0][i][1] - r2[1])))

        # Apply warpImage to small rectangular patches
        modelCropped = model[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]
        # Given a pair of triangles, find the affine transform.
        warpMat = cv2.getAffineTransform(np.float32(srcCropped), np.float32(desCropped))

        # Apply the Affine Transform just found to the src image
        userCropped = cv2.warpAffine(modelCropped, warpMat, (r2[2], r2[3]), None, flags=cv2.INTER_LINEAR,
                                     borderMode=cv2.BORDER_REFLECT_101)

        # Get mask by filling triangle
        mask = np.zeros((r2[3], r2[2], 3), dtype=np.float32)
        cv2.fillConvexPoly(mask, np.int32(desCropped), (1.0, 1.0, 1.0), 16, 0);

        # Copy triangular region of the rectangular patch to the output image
        user[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] = user[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] * (
                    (1.0, 1.0, 1.0) - mask)

        userCropped = userCropped*mask

        user[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] = user[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] + userCropped


        cv2.imshow('trial', user)


        cv2.waitKey(200)
        index += 1

    return user

def createReplaceRegion(shape , list):
    points = []
    for pos in list:
        points.append([shape[pos][0,0],shape[pos][0,1]])


    return np.matrix([l for l in points])

def get_listTriangle(model,div,srcShape , desShape):
    TList = div.getTriangleList()
    size = model.shape
    r = (0, 0, size[1], size[0])

    result  = []
    result2 = []

    listRE = srcShape[RIGHT_EYE_POINTS[0]:(RIGHT_EYE_POINTS[-1] + 1)]
    listLE = srcShape[LEFT_EYE_POINTS[0]:(LEFT_EYE_POINTS[-1] + 1)]
    listTOOTH = srcShape[TOOTH_POINTS[0]:(TOOTH_POINTS[-1] + 1)]
    listEYE = createReplaceRegion(srcShape, EYE_REGION_POINTS)
    listLIPTOP = createReplaceRegion(srcShape,TOP_LIP_POINTS)
    listLIPBOT = createReplaceRegion(srcShape,BOT_LIP_POINTS)

    for t in TList:
        pt1 = [(int)(t[0]), (int)(t[1])]
        pt2 = [(int)(t[2]), (int)(t[3])]
        pt3 = [(int)(t[4]), (int)(t[5])]

        if rect_contains(r, pt1) and rect_contains(r, pt2) and rect_contains(r, pt3):
            if (list_contains_triangle(t,listLE) == 0 and list_contains_triangle(t,listRE) == 0 and list_contains_triangle(t,listTOOTH) == 0):# and (list_contains_triangle(t,listEYE) == 1 or list_contains_triangle(t,listLIPTOP) == 1 or list_contains_triangle(t,listLIPBOT) == 1)):
                result.append(np.float32([[pt1, pt2, pt3]]))
                pt4 = np.array(desShape[get_index_point_relative(pt1, srcShape)])[0].tolist()
                pt5 = np.array(desShape[get_index_point_relative(pt2, srcShape)])[0].tolist()
                pt6 = np.array(desShape[get_index_point_relative(pt3, srcShape)])[0].tolist()
                result2.append(np.float32([[pt4, pt5, pt6]]))

    return result , result2

def get_index_point_relative(point,shape):
    for idx , p in enumerate(shape):
        # print(p)
        # print(point)
        if point == [p[0,0], p[0,1]]:
            #print(idx)
            return idx
