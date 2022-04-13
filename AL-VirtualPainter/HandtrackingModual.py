import cv2
import mediapipe as mp
import time
import math


class handDetector():
    def __init__(self, mode=False, maxHands=3, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4,8, 12,16,20]

    def findHands(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                # if id == 8:
                #     cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return self.lmList

    def findAngle(self, img, pointList, draw=True):
        drawList = []

        for point in pointList:
            if len(self.lmList):
                i, x, y = self.lmList[point][0:]
                cv2.circle(img, (x, y), 10, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, (x, y), 15, (0, 255, 0), 2)
                drawList.append([i, x, y])

                if draw:
                    n = len(drawList)
                    for i in range(n):
                        if i+1 == n:
                            break
                        cv2.line(
                            img, drawList[i][1:], drawList[i+1][1:], (0, 0, 255), 3)

        # Calculate the Angle:
        if len(drawList):
            angle = math.degrees(math.atan2((drawList[-1][2])-(drawList[-2][2]), (drawList[-1][1])-(
                drawList[-2][1]))-math.atan2((drawList[0][2])-(drawList[-2][2]), (drawList[0][1])-(drawList[-2][1])))
            if angle < 0:
                angle += 360
            cv2.putText(img, str(int(angle)), ((
                drawList[1][1]-50), (drawList[1][2]+50)), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            return angle

    def fingersUp(self):
        fingers = []
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[4]-3][1]:  # detect right hands

            # print("Now left hand is up and the count is: ")
            # Thumb detector
            if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            #  Find the fingers Situations except thumb
            for id in range(1, 5):
                if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            # print(fingers)
            totalFingers = fingers.count(1)
            print(totalFingers)

        else:  # detect left hands
            # print("Now right hand is up and the count is: ")
            if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            #  Find the fingers Situations except thumb
            for id in range(1, 5):
                if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        return fingers


def main():
    pTime = 0  # past time
    cTime = 0  # Current time
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print("The finger print location is : ", lmList[8])

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("Showing", img)
        cv2.waitKey(1000)


if __name__ == "__main__":
    main()
