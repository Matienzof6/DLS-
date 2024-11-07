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


detectorPaths = {
	"face": "haarcascade_frontalface_default.xml",
	"eyes": "haarcascade_eye.xml",
	"smile": "haarcascade_smile.xml",
}

print("[INFO] loading haar cascades...")
detectors = {}

# loop over our detector paths
for (name, path) in detectorPaths.items():
	# load the haar cascade from disk and store it in the detectors dictionary
	path = os.path.sep.join([args["cascades"], path])
	detectors[name] = cv2.CascadeClassifier(path)

print("[INFO] starting video stream...")
device = cv2.VideoCapture(0)
time.sleep(2.0)
if not device.isOpened():
    print("No se puede abrir la camara")
    exit()
while True:
    cam, frame = device.read()
    if not cam:
        print("No se pudo leer de la cámara")
        break
    cv2.imshow("Image", frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faceRects = detectors["face"].detectMultiScale(
		gray, scaleFactor=1.05, minNeighbors=5, minSize=(30, 30),
		flags=cv2.CASCADE_SCALE_IMAGE)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
device.release()
cv2.destroyAllWindows()