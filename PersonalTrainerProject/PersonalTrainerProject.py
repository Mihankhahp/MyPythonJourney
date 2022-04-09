import cv2
from matplotlib.pyplot import draw
import mediapipe as mp
import time
import PoseEstimationModual as pem


detector = pem.poseDetector(detectionCon=0.75)
cap = cv2.VideoCapture(0)
pTime = 0


while True:

    success, img = cap.read()
    img = detector.findPose(img, draw=False)
    lmList = detector.getPosition(img, draw=False)
    if len(lmList) != 0:
        detector.findAngle(img, pointList=[12, 14, 16])
        detector.findAngle(img, pointList=[11, 13, 15])

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (70, 50),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    imgResized = cv2.resize(img, (960, 650))
    cv2.imshow("Personal Trainer Project", imgResized)
    cv2.waitKey(1)
