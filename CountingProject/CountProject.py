from traceback import print_stack
import cv2
import mediapipe as mp
import time
import HandtrackingModual as htm
import os


cap = cv2.VideoCapture(0)
pTime = 0

#  import the pictures from the path
folderPath = "CountingProject\FingerImage"
myList = os.listdir(folderPath)
# print(myList)


# Looping in our folder of pictures to find each pic path
overlayList = []
for imgPath in myList:
    pic = cv2.imread(f'{folderPath}/{imgPath}')
    # print(f'{folderPath}/{imgPath}')
    overlayList.append(pic)

detector = htm.handDetector(detectionCon=0.75)
tipsIds = [4, 8, 12, 16, 20]
while True:

    success, img = cap.read()

    #  Find the hands
    img = detector.findHands(img)
    lmList, handNo = detector.findPosition(img, draw=False)

    fingers = []
    if len(lmList) != 0:
        #  Find Which hands are up
        if lmList[tipsIds[0]][1] > lmList[tipsIds[4]-3][1]:  # detect right hands

            print("Now right hand is up and the count is: ")
            # Thumb detector
            if lmList[tipsIds[0]][1] > lmList[tipsIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            #  Find the fingers Situations except thumb
            for id in range(1, 5):
                if lmList[tipsIds[id]][2] < lmList[tipsIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            # print(fingers)
            totalFingers = fingers.count(1)
            print(totalFingers)

        else:  # detect left hands
            print("Now Left hand is up and the count is: ")
            if lmList[tipsIds[0]][1] < lmList[tipsIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            #  Find the fingers Situations except thumb
            for id in range(1, 5):
                if lmList[tipsIds[id]][2] < lmList[tipsIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            # print(fingers)
            totalFingers = fingers.count(1)
            print(totalFingers)

        h, w, c = overlayList[totalFingers-1].shape
        img[0:h, 0:w] = overlayList[totalFingers-1]
        cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0),cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45, 375),
                cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 25)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (400, 70),
                cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
    cv2.imshow("Counting Projects", img)
    cv2.waitKey(1000)
