import cv2
import imutils
import argparse
import time
from imutils.video import VideoStream
import os
import subprocess

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


# initialize the video stream and allow the camera sensor to warm up

print("[INFO] starting video stream...")
device = VideoStream(src=0).start()
time.sleep(2.0)

# variable to control the stop statement

is_paused = False

# loop over the frames from the video stream
while True:
    # grab the frame from the video stream, resize it, and convert it to grayscale
    frame = device.read()
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # perform face detection using the appropriate haar cascade
    faceRects = detectors["face"].detectMultiScale(
		gray, scaleFactor=1.05, minNeighbors=5, minSize=(30, 30),
		flags=cv2.CASCADE_SCALE_IMAGE)
    if len(faceRects) == 0:
        # Pause the video only if the video is not paused yet
        if not is_paused:
            subprocess.run(['playerctl', 'play-pause'])
            print("Faces are no longer detected, video paused")
            is_paused = True  # change the state to "paused" to avoid loops
    else:
        # If the faces are detected the video will continue
    
    # loop over the face bounding boxes
        for (fX, fY, fW, fH) in faceRects:
            # extract the face ROI
            faceROI = gray[fY:fY+ fH, fX:fX + fW]
            # apply eyes detection to the face ROI
            eyeRects = detectors["eyes"].detectMultiScale(
                    faceROI, scaleFactor=1.1, minNeighbors=10,
                    minSize=(15, 15), flags=cv2.CASCADE_SCALE_IMAGE)
            # loop over the eye bounding boxes
            for (eX, eY, eW, eH) in eyeRects:
                # draw the eye bounding box
                ptA = (fX + eX, fY + eY)
                ptB = (fX + eX + eW, fY + eY + eH)
                cv2.rectangle(frame, ptA, ptB, (0, 0, 255), 2)
            # draw the face bounding box on the frame
            cv2.rectangle(frame, (fX, fY), (fX + fW, fY + fH),
                (0, 255, 0), 2)





# show the output frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
    # do a bit of cleanup



cv2.destroyAllWindows()
device.stop()