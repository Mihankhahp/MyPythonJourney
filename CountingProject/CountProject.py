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
    print(f'{folderPath}/{imgPath}')
    overlayList.append(pic)


while True:

    success, img = cap.read()

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'{str(int(fps))}', (10, 70),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    cv2.imshow("Counting Projects", img)
    cv2.waitKey(1)
