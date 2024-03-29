import dlib
import cv2
from imutils import face_utils
import numpy as np
import argparse
import imutils

ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())
path = 'shape_predictor_68_face_landmarks.dat'

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(path)

# load the input image, resize it, and convert it to grayscale
image = cv2.imread('face1.jpg')
image = imutils.resize(image, width=500)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# detect faces in the grayscale image
rects = detector(gray, 1)


# loop over the face detections
for (i, rect) in enumerate(rects):

	shape = predictor(gray, rect)
	shape = face_utils.shape_to_np(shape)

	(x, y, w, h) = face_utils.rect_to_bb(rect)
	cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
	cv2.putText(image, "Face #{}".format(i + 1), (x - 10, y - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

no_faces  = i+1

print("No. of faces detected : ", no_faces)
cv2.imshow("Output", image)
cv2.waitKey(0)
