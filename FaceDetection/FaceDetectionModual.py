import cv2
import mediapipe as mp
import time


class FaceDetection():
    def __init__(self, minDetection=0.5):
        self.minDetection = minDetection
        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection(
            self.minDetection)

    def findFace(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceDetection.process(imgRGB)
        bboxs = []
        if self.results.detections:
            for id, detection in enumerate(self.results.detections):
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, ic = img.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin *
                                                 ih), int(bboxC.width * iw), int(bboxC.height * ih)
                bboxs.append([id, bbox, int((detection.score[0])*100)])
                if draw:
                    img = self.fancyDraw(img, bbox)
                    cv2.putText(img, f'{int((detection.score[0])*100)}%', (bbox[0], bbox[1]-20),
                                cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        return img, bboxs

    def fancyDraw(self, img, bbox, l=30, t=5, rtl=1):
        x, y, w, h = bbox
        x1, y1 = x+w, y+h
        cv2.rectangle(img, bbox, (0, 255, 0), rtl)
        # Top Left
        cv2.line(img, (x, y), (x+l, y), (0, 255, 0), t)
        cv2.line(img, (x, y), (x, y+l), (0, 255, 0), t)
        # Top Right
        cv2.line(img, (x1, y), (x1-l, y), (0, 255, 0), t)
        cv2.line(img, (x1, y), (x1, y+l), (0, 255, 0), t)
        # Bottom Left
        cv2.line(img, (x, y1), (x+l, y1), (0, 255, 0), t)
        cv2.line(img, (x, y1), (x, y1-l), (0, 255, 0), t)
        # Bottom Right
        cv2.line(img, (x1, y1), (x1-l, y1), (0, 255, 0), t)
        cv2.line(img, (x1, y1), (x1, y1-l), (0, 255, 0), t)
        return img


def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    detector = FaceDetection()
    while True:
        success, img = cap.read()
        img, bboxs = detector.findFace(img)
        print(bboxs)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, f'FPS: {int(fps)}', (20, 70),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        cv2.waitKey(1)
        cv2.imshow("Face Detection Project", img)


if __name__ == "__main__":
    main()
