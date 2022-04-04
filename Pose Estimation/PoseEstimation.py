import cv2
import mediapipe as mp
import time


# Create the Object for Detecting pose
mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils


# Make entry as a img which could be a video, picture , real time webcame.
cap = cv2.VideoCapture("PoseVideo/Vid2.mp4",)

# cap = cv2.VideoCapture(0) ==> realtime webcam 


pTime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = pose.process(imgRGB)
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks,
                              mpPose.POSE_CONNECTIONS)
        # Detect each land marks position and put it in cx and cy                      
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y*h)
            cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (70, 50),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    imgResized = cv2.resize(img, (960, 540))
    cv2.imshow("PoseEstimate", imgResized)
    cv2.waitKey(1)
