import cv2
import numpy as np
import time
import math
import mediapipe as mp
import HandTrackingModule as htm

from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cap = cv2.VideoCapture(0)
wCam, hCam = 640, 480
cap.set(3, wCam)
cap.set(4,hCam)

pTime = 0

detector  = htm.handDetector(detectionCon=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
print(volRange)
minVol = volRange[0]
maxVol = volRange[1]

volBar = 400
vol = 0
volBarPer = 0

while(cap.isOpened()):
    _, frame = cap.read()

    frame = detector.findHands(frame)
    landmark_lst = detector.findPosition(frame,draw=False)

    if len(landmark_lst) !=0:
        #print(landmark_lst[4], landmark_lst[8])
        x1, y1 = landmark_lst[4][1], landmark_lst[4][2]
        x2, y2 = landmark_lst[8][1], landmark_lst[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(frame, (x1, y1), 15, (255,0,255), cv2.FILLED)
        cv2.circle(frame, (x2, y2), 15, (255,0,255), cv2.FILLED)
        cv2.line(frame, (x1, y1), (x2, y2), (255,0,255),3)
        cv2.circle(frame, (cx, cy), 15, (255,0,255), cv2.FILLED)

        # length of line
        length = math.hypot(x2 - x1, y2 - y1)
        #print(length)

        # Hand range 50 - 300
        # System Volume range -65.25 - 0.0
        # cvt Hand range to System volume range
        vol = np.interp(length, [50, 300], [minVol, maxVol])
        volBar = np.interp(length, [50, 300], [400, 150])
        volBarPer = np.interp(length, [50, 300], [0, 100])
        #print(int(length),vol)
        volume.SetMasterVolumeLevel(vol, None)


        if length <= 50:
            cv2.circle(frame, (cx, cy), 15, (0,255,0), cv2.FILLED)

    cv2.rectangle(frame,(50,150),(85,400),(255,0,0),3)
    cv2.rectangle(frame,(50,int(volBar)),(85,400),(255,0,0),cv2.FILLED)
    cv2.putText(frame,f'{int(volBarPer)} %',(40,450),cv2.FONT_HERSHEY_COMPLEX,
                    1,(255,0,0),2)


    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(frame,f'FPS: {int(fps)}',(40,50),cv2.FONT_HERSHEY_COMPLEX,
                    1,(255,0,0),2)

    cv2.imshow('Frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()