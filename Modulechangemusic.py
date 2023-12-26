import numpy as np
import cv2
import time
import hand as htm
import os
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
import math
from ctypes import cast , POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities , IAudioEndpointVolume
pTime = 0 
cap = cv2.VideoCapture(0)
detector = htm.handDetector(detectionCon=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
volume = cast(interface,POINTER(IAudioEndpointVolume))
volRange =volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

while(True):
    ret, frame = cap.read()
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame,draw=False)

    if (len(lmList) != 0):
        x1 ,y1= lmList[4][1], lmList[4][2]
        x2 ,y2 = lmList[8][1], lmList[8][2] 

        # vẽ điểm tròn trên ngón cái
        cv2.circle(frame,(x1,y1),15,(155,155,155),-1)
        # vẽ điểm tròn trên ngón trỏ
        cv2.circle(frame,(x2,y2),15,(155,100,155),-1)
        # nối hai điểm
        cv2.line(frame,(x1,y1),(x2,y2),(255,3,255),3)
        # vẽ hình tròn ở giữa
        cx,cy = (x1 + x2)//2,(y1 + y2)//2
        cv2.circle(frame,(cx, cy),10,(255,0,255),-1)
        # độ dài đoạn thẳng
        doDaiDoanThang = math.hypot(x2 - x1, y2-y1)

        # khoảng cách giữa hai điểm vào khoảng 30-230
        # dải âm thanh trên máy chạy từ -74 --> 0
        vol = np.interp(doDaiDoanThang,[30,200],[minVol,maxVol]) 
        volBar = np.interp(doDaiDoanThang,[30,200],[400,150])
        voltyle = np.interp(doDaiDoanThang,[30,200],[0,100])
        volume.SetMasterVolumeLevel(vol,None) 
        if doDaiDoanThang < 30:
            cv2.circle(frame ,(cx, cy),10,(255,0,0),-1)

        cv2.rectangle(frame ,(50,150),(100,400),(0,0,255),3)
        cv2.rectangle(frame ,(50,int(volBar)),(100,400),(0,255,0),-1)
        # show % volume
        cv2.putText(frame,f"FPS:{int(voltyle)} %",(50,450),cv2.FONT_HERSHEY_PLAIN,3,(0,0,0),4)

    # Viết ra FPS
    cTime = time.time() 
    fps = 1/(cTime - pTime) 
    pTime =  cTime 
    # show fps trên màn hình
    print(type(fps))
    cv2.putText(frame,f"FPS:{int(fps)}",(150,70),cv2.FONT_HERSHEY_PLAIN,3,(0,0,0),5)

    cv2.imshow("Khung hinh ^.^ " , frame)
    if (cv2.waitKey(1) == ord('l')):
        break
cap.release() # giải phóng camera
cv2.destroyAllWindows()#  thoát tất cả các cửa sổ
