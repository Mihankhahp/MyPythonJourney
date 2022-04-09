import cv2
from cv2 import line
import mediapipe as mp
import time
import math


class poseDetector():

    def __init__(self, mode=False, model_complexity=1, upBody=False, smooth=True, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.model_complexity = model_complexity
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(
            self.mode, self.model_complexity, self.upBody, self.smooth, self.detectionCon, self.trackCon)

    def findPose(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img

    def getPosition(self, img, personsDetected=0, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

        return self.lmList

    # Find angle between the point number 1, 2, 3
    def findAngle(self, img, pointList, draw=True):
        drawList = []

        for point in pointList:
            i, x, y = self.lmList[point][0:]
            cv2.circle(img, (x, y), 10, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (x, y), 15, (0, 255, 0), 2)
            drawList.append([i, x, y])

        drawList.sort()
        if draw:
            n = len(drawList)
            for i in range(n):
                if i+1 == n:
                    break
                cv2.line(
                    img, drawList[i][1:], drawList[i+1][1:], (0, 0, 255), 3)

        # Calculate the Angle:
        angle = math.degrees(math.atan2((drawList[-1][2])-(drawList[-2][2]), (drawList[-1][1])-(
            drawList[-2][1]))-math.atan2((drawList[0][2])-(drawList[-2][2]), (drawList[0][1])-(drawList[-2][1])))
        if angle < 0:
            angle += 360
        cv2.putText(img, str(int(angle)), ((
            drawList[1][1]-50), (drawList[1][2]+50)), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

        return angle


def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    detector = poseDetector()

    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.getPosition(img)
        if len(lmList) != 0:
            cv2.circle(img, (lmList[0][1], lmList[0][2]),
                       7, (255, 0, 255), cv2.FILLED)
            print("The location is : ", lmList[0])

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (70, 50),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        imgResized = cv2.resize(img, (960, 540))
        cv2.imshow("PoseEstimate", imgResized)
        cv2.waitKey(100)


if __name__ == "__main__":
    main()
