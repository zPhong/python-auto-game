import cv2
import dlib
import numpy as np
import copy
from scipy.spatial import distance as dist
import sys

PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat"

# data in http://matthewearl.github.io/2015/07/28/switching-eds-with-python/
FEATHER_AMOUNT = 11

FACE_POINTS = list(range(17, 68))
MOUTH_POINTS = list(range(48, 61))
RIGHT_BROW_POINTS = list(range(17, 22))
LEFT_BROW_POINTS = list(range(22, 27))
RIGHT_EYE_POINTS = list(range(36, 42))
LEFT_EYE_POINTS = list(range(43, 48))
TOOTH_POINTS = list(range(60, 68))
NOSE_POINTS = list(range(27, 36))
JAW_POINTS = list(range(0, 17))

# element will be overlaid.
OVERLAY_POINTS = [
    LEFT_EYE_POINTS + RIGHT_EYE_POINTS + LEFT_BROW_POINTS + RIGHT_BROW_POINTS,
    NOSE_POINTS + MOUTH_POINTS,
]

# Points used to line up the images.
ALIGN_POINTS = (LEFT_BROW_POINTS + RIGHT_EYE_POINTS + LEFT_EYE_POINTS +
                               RIGHT_BROW_POINTS + NOSE_POINTS + MOUTH_POINTS)


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(PREDICTOR_PATH)

EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 3

def shape_to_np(shape, dtype="int"):
    # initialize the list of (x, y)-coordinates
    coords = np.zeros((68, 2), dtype=dtype)

    # loop over the 68 facial landmarks and convert them
    # to a 2-tuple of (x, y)-coordinates
    for i in range(0, 68):
        coords[i] = (shape.part(i).x, shape.part(i).y)

    # return the list of (x, y)-coordinates
    return coords


# Check if a point is inside a rectangle
def rect_contains(rect, point):
    if point[0] < rect[0]:
        return False
    elif point[1] < rect[1]:
        return False
    elif point[0] > rect[2]:
        return False
    elif point[1] > rect[3]:
        return False
    return True


def draw_delaunay(img, subdiv, delaunay_color):
    triangleList = subdiv.getTriangleList();
    size = img.shape
    r = (0, 0, size[1], size[0])

    for t in triangleList:

        pt1 = (t[0], t[1])
        pt2 = (t[2], t[3])
        pt3 = (t[4], t[5])

        if rect_contains(r, pt1) and rect_contains(r, pt2) and rect_contains(r, pt3):
            cv2.line(img, pt1, pt2, delaunay_color, 1)
            cv2.line(img, pt2, pt3, delaunay_color, 1)
            cv2.line(img, pt3, pt1, delaunay_color, 1)

def get_delaunay_array(img ,shape):
    size = img.shape

    subrect = (0, 0, size[1], size[0])
    subdiv = cv2.Subdiv2D(subrect);
    points = []

    for p in shape:
         #if rect_contains(subrect, (p[0,0], p[0,1])):
        points.append((p[0,0], p[0,1]))

    for point in points:
        subdiv.insert(point)
    #cv2.imshow((str)(size[1]),img)
    return subdiv


def get_landmarks_pts(image):
    clone = copy.copy(image)
    gray = cv2.cvtColor(clone, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 1)
    for (i, rect) in enumerate(rects):
        rectImg = copy.copy(clone)
        shape = predictor(gray, rect)
        shape = shape_to_np(shape)
        return shape

def draw_Contour(image,shape):

    mounth_top =[]
    mounth_top.extend(shape[MOUTH_TOP_UP_POINTS[0]:(MOUTH_TOP_UP_POINTS[-1]+1)].tolist())
    mounth_top.extend(shape[MOUTH_TOP_DOWN_POINTS[0]:(MOUTH_TOP_DOWN_POINTS[-1] +1)].tolist())

    cv2.drawContours(image, [cv2.convexHull(shape[LEFT_EYE_POINTS[0]:(LEFT_EYE_POINTS[-1]+1)])], -1, (0, 255, 0), 1)
    cv2.drawContours(image, [cv2.convexHull(shape[RIGHT_EYE_POINTS[0]:(RIGHT_EYE_POINTS[-1]+1)])], -1, (0, 255, 0), 1)
    cv2.drawContours(image, [cv2.convexHull(np.asarray(mounth_top))], -1, (255, 255, 0), 1)

def get_landmarks(image , name):

    clone = copy.copy(image)
    gray = cv2.cvtColor(clone, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 1)

    # loop over the face detections
    for (i, rect) in enumerate(rects):
        rectImg = copy.copy(clone)

        shape = predictor(gray,rect)
        shape = shape_to_np(shape)

        # for (x, y) in shape:
        #     # get_face_mask(copy.copy(rectImg), np.matrix([[p.x, p.y] for p in predictor(image, rect).parts()]))
        #     cv2.circle(image, (x, y), 3, (0, 255, 0), -1)

        # show the output image with the face detections + facial landmarks
        if name == 'Model':
            cv2.imshow(name,image);

    return np.matrix([[p.x, p.y] for p in predictor(rectImg, rects[0]).parts()]) , rects[0]


def transformation_from_points(points1, points2):
    points1 = points1.astype(np.float64)
    points2 = points2.astype(np.float64)

    c1 = np.mean(points1, axis=0)
    c2 = np.mean(points2, axis=0)
    points1 -= c1
    points2 -= c2

    s1 = np.std(points1)
    s2 = np.std(points2)
    points1 /= s1
    points2 /= s2

    U, S, Vt = np.linalg.svd(points1.T * points2)
    R = (U * Vt).T

    return np.vstack([np.hstack(((s2 / s1) * R,
                                       c2.T - (s2 / s1) * R * c1.T)),
                         np.matrix([0., 0., 1.])])

def warp_im(im, M, dshape):
    output_im = np.zeros(dshape, dtype=im.dtype)
    cv2.warpAffine(im,
                   M[:2],
                   (dshape[1], dshape[0]),
                   dst=output_im,
                   borderMode=cv2.BORDER_TRANSPARENT,
                   flags=cv2.WARP_INVERSE_MAP)
    return output_im