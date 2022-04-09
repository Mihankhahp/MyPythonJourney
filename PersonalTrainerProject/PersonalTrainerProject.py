import cv2
import mediapipe as mp
import time
import PoseEstimationModual as pem


cap = cv2.VideoCapture(0)
pTime = 0


while True:
    success, img = cap.read()

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (70, 50),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    imgResized = cv2.resize(img, (960, 540))
    cv2.imshow("PoseEstimate", imgResized)
    cv2.waitKey(100)
    cv2.imshow("Personal Trainer Project", img)
    cv2.waitKey(1)
