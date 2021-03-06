import os
import cv2
from cv2 import FILLED
import mediapipe as mp
import time
import math
import numpy as np
import HandtrackingModual as htm


# Initialization
####################################################################################

cap = cv2.VideoCapture(0)
pTime = 0

# Import pictures
folderPath = "D:\MyPythonJourney\AL-VirtualPainter\VirtuallPaintingPictures"
myList = os.listdir(folderPath)

# Make each picture available and store it in list
overLayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overLayList.append(image)

# Default values
header = overLayList[0]
drawColor = (0, 255, 0)
brushTickness = 15
eraserTickness = 150
xp, yp = 0, 0
imgCanvas = np.zeros((540, 960, 3), np.uint8)


while True:
    success, img = cap.read()
    detector = htm.handDetector()
    img = cv2.resize(img, (960, 540))
    # Flip the image to synce with our hand direction
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList):

        # tip of index and middle fingers
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # Check which fingers are up
        fingers = detector.fingersUp()

        # Selecting method
        if fingers[1] and fingers[2]:

            # Refresh the coordinates when the mode had changed
            xp, yp = 0, 0

            # When fingers go in header
            if y1 < 85:
                # Green
                if 320 < x1 < 389:
                    header = overLayList[0]
                    drawColor = (0, 255, 0)
                # Red
                elif 434 < x1 < 494:
                    header = overLayList[1]
                    drawColor = (0, 0, 255)
                # Blue
                elif 549 < x1 < 609:
                    header = overLayList[2]
                    drawColor = (255, 0, 0)
                # Eraser
                elif 847 < x1 < 922:
                    header = overLayList[3]
                    drawColor = (0, 0, 0)
            cv2.rectangle(img, (x1, y1-15), (x2, y2+15),
                          drawColor, cv2.FILLED)

        # Drawing method
        if fingers[1] and fingers[2] == False:

            cv2.circle(img, (x1, y1), 10, drawColor, cv2.FILLED)

            if xp == 0 and yp == 0:

                # Refreshing every time
                xp, yp = x1, y1

            # Eraser
            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserTickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1),
                         drawColor, eraserTickness)

            # Other Color
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushTickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1),
                         drawColor, brushTickness)

            xp, yp = x1, y1


# Combine img and imgCanvas

    # Conver imgCanvas to gray image
    imageGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)

    # Conver imgGray to image invers
    # in imgInv everythings are black and white ==> drawing will be black and background will be White IN CONTRAST the imgCanva which is background black and drwing colorful
    _, imgInv = cv2.threshold(imageGray, 50, 255, cv2.THRESH_BINARY_INV)

    # Conver imgInv to BGR from Gray
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)

    # add imgInv and img
    # Add drawing black on img
    img = cv2.bitwise_and(img, imgInv)

    # Put the colorful drawing on the img which was combined with imgInv
    img = cv2.bitwise_or(img, imgCanvas)


# Setting the header image
    img[0:85, 0:960] = header

# Showing FPS
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS:{int(fps)}', (20, 70),
                cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

    # cv2.addWeighted(img, 0.5, imgCanvas, 0.5,0)

    cv2.imshow("AL-VirtualPainter", img)
    # cv2.imshow("AL-VirtualPainterCanvas", imgCanvas)
    cv2.waitKey(1)
