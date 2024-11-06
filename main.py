import cv2
import imutils
import argparse
import time
from imutils.video import VideoStream
import os



ap = argparse.ArgumentParser()
ap.add_argument("-c", "--cascades", type=str, default="cascades",
	help="path to input directory containing haar cascades")
args = vars(ap.parse_args())


device = cv2.VideoCapture(0)
if not device.isOpened():
    print("No se puede abrir la camara")
    exit()
while True:
    cam, frame = device.read()
    if not cam:
        print("No se pudo leer de la cámara")
        break
    cv2.imshow("Image", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
device.release()
cv2.destroyAllWindows()