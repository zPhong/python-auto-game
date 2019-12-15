import numpy as np
import cv2

from face_detect_landmark import get_landmarks



# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades

# https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
eye_cascade = cv2.CascadeClassifier('parojosG.xml')#'haarcascade_eye.xml')
smile_cascde = cv2.CascadeClassifier('haarcascade_smile.xml')
glass = cv2.imread('images/glass.png', -1)
model = cv2.imread('images/model.jpg', 1)


cap = cv2.VideoCapture(0)
while 1:
    ret, img = cap.read()
    img = cv2.flip(img,1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    #read_im_and_landmarks(img)
    get_landmarks(model , "Model")

    for (x, y, w, h) in faces:

        get_landmarks(img , "User")
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)


        eyes_gray = gray[y:y +  (int)(h), x:x + w]
        eyes_color = img[y:y +  (int)(h), x:x + w]

        # eyes = eye_cascade.detectMultiScale(eyes_gray)
        # for (ex, ey, ew, eh) in eyes:
        #     # glass = cv2.resize(glass, (w,(int)(eh*1.2)),interpolation = cv2.INTER_CUBIC)
            # ex = x
            # ew = w
            # gh, gw, gc = glass.shape
            # for i in range(0,gh):
            #     for j in range(0,gw):
            #         if glass[i,j][3] != 0:
            #             eyes_color[ey + i , j][0] = glass[i,j][0]
            #             eyes_color[ey + i , j][1] = glass[i,j][1]
            #             eyes_color[ey + i , j][2] = glass[i,j][2]
            # # cv2.rectangle(eyes_color, (ex - (int)((w - ew)/2) , ey), (ex + ew  + (int)((w - ew)/2), ey + eh), (0, 255, 0), 2)
            # cv2.circle(eyes_color, (ex, ey), 1, (0, 0, 255))

        # smiles_gray = gray[y + (int)(h * 2/3):y + (int)(h), x:x + w]
        # smiles_color = img[y + (int)(h * 2/3):y + (int)(h), x:x + w]
        #
        # smiles = smile_cascde.detectMultiScale(smiles_gray)
        # # for (sx, sy, sw, sh) in smiles:
        #     cv2.imshow('smile',smiles_gray)
        #     cv2.rectangle(smiles_color, (sx, sy), (sx + sw, sy + sh), (0, 0 , 255), 2)

    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
