import cv2
from matplotlib.pyplot import draw
import mediapipe as mp
import time
import PoseEstimationModual as pem
import numpy as np


detector = pem.poseDetector(detectionCon=0.75)
cap = cv2.VideoCapture(0)
pTime = 0
count = 0
dir = 0


while True:

    success, img = cap.read()
    img = detector.findPose(img, draw=False)
    lmList = detector.getPosition(img, draw=False)
    if len(lmList) != 0:
        angle = detector.findAngle(img, pointList=[12, 14, 16])  # Right Arm
        # angle = detector.findAngle(img, pointList=[11, 13, 15])  # Left Arm
        per = np.interp(angle, (195, 300), (0, 100))
         
        # print(per)
        bar = int(np.interp(angle, (195, 300), (400, 150)))
        # Check for dumbbell curls:
        color = (255, 0, 255)
        if per == 100:
            color = (0, 255, 0)
            if dir == 0:
                count += (0.5)
                dir = 1
        if per== 0:
            color = (0, 255, 0)
            if dir == 1:
                count += (0.5)
                dir = 0
        cv2.rectangle(img, (600, 150), (620, 400), (0,255,0), 3)
        cv2.rectangle(img, (600, bar),(620, 400), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)}%', (500, 450),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

        cv2.putText(img, str(int(count)), (50, 400),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime



    imgResized = cv2.resize(img, (1000, 700))
    cv2.imshow("Personal Trainer Project", imgResized)
    cv2.waitKey(1)
