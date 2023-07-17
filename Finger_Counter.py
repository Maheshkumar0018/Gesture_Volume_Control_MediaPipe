import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
import os

cap = cv2.VideoCapture(0)
wCam, hCam = 640, 480
cap.set(3,wCam)
cap.set(4,hCam)

folder_path = 'fingersimg'
myList = os.listdir(folder_path)
overlayList = []

for imPath in myList:
    images = cv2.imread(f'{folder_path}/{imPath}')
    overlayList.append(images)

detector  = htm.handDetector(detectionCon=0.7)
tipIds = [4,8,12,16,20]

pTime = 0

while(cap.isOpened()):
    _, frame = cap.read()

    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame, draw=False)

    if len(lmList) !=0:
        fingers = []
        # right-hand thumb 
        if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
            fingers.append(1)
        # right-hand 4 fingers
        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        totalfingers = fingers.count(1)

        h, w, c = overlayList[0].shape
        frame[0:h,0:w] = overlayList[totalfingers - 1]

        cv2.rectangle(frame,(20,255),(170,425),(0,255,0),cv2.FILLED)
        cv2.putText(frame,str(totalfingers),(45,375),cv2.FONT_HERSHEY_PLAIN,
                    10,(255,0,0),25)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(frame,f'FPS: {int(fps)}',(400,70),cv2.FONT_HERSHEY_COMPLEX,
                    1,(255,0,0),2)
    cv2.imshow('Frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()