import cv2
from cv2 import line
import mediapipe as mp
import time
import numpy as np
import HandtrackingModual as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


wCam, hCam = 640, 480

detector = htm.handDetector(detectionCon=0.7)


# initialization code from the library

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# volume.GetMute()
# volume.GetMasterVolumeLevel()


volRange = volume.GetVolumeRange()  # fom -74 - 0
minVol = volRange[0]
maxVol = volRange[1]


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    # Its already drawing in findHands
    lmList = detector.findPosition(img, draw=False)
    vol = 0
    volBar = 400
    volPerc = 0

    if len(lmList) != 0:
        # print("ittttttttttttttttttttttttttttts", lmList)

        # print(lmList[4], lmList[8])
        # The point of Tomb and Index finger
        x4, y4 = lmList[4][1], lmList[4][2]
        x8, y8 = lmList[8][1], lmList[8][2]
        # find the center of line between this points
        cx, cy = (x4+x8)//2, (y4+y8)//2

        cv2.circle(img, (x4, y4), 7, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x8, y8), 7, (255, 0, 255), cv2.FILLED)
        cv2, line(img,  (x8, y8), (x4, y4), (0, 255, 0), 2)

        cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x8-x4, y8-y4)
        vol = np.interp(length, [15, 114], [minVol, maxVol])
        volBar = np.interp(length, [15, 114], [400, 150])
        volPerc = np.interp(length, [15, 114], [0, 100])
        volume.SetMasterVolumeLevel(vol, None)

        if length < 25:
            cv2.circle(img, (cx, cy), 7, (255, 0, 0), cv2.FILLED)
    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPerc)}%', (40, 450),
                cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
    # print(length)
    # print("fin")

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (40, 50),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    # imgResized = cv2.resize(img, (960, 540))

    cv2.imshow("Volume Controler", img)
    cv2.waitKey(1)
