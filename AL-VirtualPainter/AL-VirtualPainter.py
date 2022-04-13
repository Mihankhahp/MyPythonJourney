import os
import cv2
from cv2 import FILLED
import mediapipe as mp
import time
import math
import numpy as np
import HandtrackingModual as htm


cap = cv2.VideoCapture(0)
pTime = 0


folderPath = "D:\MyPythonJourney\AL-VirtualPainter\VirtuallPaintingPictures"
myList = os.listdir(folderPath)
# print(myList)


overLayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overLayList.append(image)

# print(len(overLayList))
header = overLayList[0]


while True:
    success, img = cap.read()
    detector = htm.handDetector(detectionCon=0.75)
    img = cv2.resize(img, (960, 540))
# Flip the image to synce with our hand direction
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    # angle= detector.findAngle()
    if len(lmList):

        # tip of index and middle fingers
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # Check which fingers are up
        fingers = detector.fingersUp()
        # print(fingers)
        if fingers[1] and fingers[2]:
            cv2.rectangle(img, (x1, y1-15), (x2, y2+15),
                          (255, 0, 255), cv2.FILLED)
            if y1 < 85:
                if 320 < x1 < 389:
                    header = overLayList[0]
                    # print("overLayList[0]")
                elif 434 < x1 < 494:
                    header = overLayList[1]
                    # print("overLayList[1]")
                elif 549 < x1 < 609:
                    header = overLayList[2]
                    # print("overLayList[2]")
                elif 664 < x1 < 723:
                    header = overLayList[3]
                    # print("overLayList[3]")
                elif 845 < x1 < 922:
                    header = overLayList[4]
                    # print("overLayList[4]")

            # print("selection mode")
        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)

            print("Drawing mode")

# Setting the header image
    img[0:85, 0:960] = header

# Showing FPS
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS:{int(fps)}', (20, 70),
                cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

    cv2.imshow("AL-VirtualPainter", img)
    cv2.waitKey(100)
