import cv2
import time
import os
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
import os
import mediapipe as mp
import hand as htm

pTime = 0 
cap = cv2.VideoCapture(0)
folderPath = "F:\\projectPython\\bai5\\finger\\Fingers"
lst = os.listdir(folderPath) 
lst2 =[]
for i in lst:
    image = cv2.imread(f"{folderPath}/{i}") 
    lst2.append(image)

detector = htm.handDetector(detectionCon=0.55) 
finger_id = [4,8,12,16,20] 
while(True):
    ret, frame = cap.read()
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame,draw=False)
    print(lmList)

    # THAO TÁC COI NGÓN TAY 
    
    if len(lmList)!= 0:
        fingers = []
        #1.Viết cho ngón cái(điểm 4 nằm trái hay phải điểm 3)
        if (lmList[finger_id[0]][1] < lmList[finger_id[0]-1][1]): #[4,569,270] [3,584,329] lấy ra giá trị 569 < 584
             fingers.append(1) # ngón mở thì append số 1
        else:
            fingers.append(0) # ngón đóng thì append số 0

        #2.Viết cho trường hợp 4 ngón dài trước vì 4 ngón dài ngập xuống được
        for i in range(1,5):
            if (lmList[finger_id[i]][2] < lmList[finger_id[i]-2][2]): #[8,569,270] [6,584,329] lấy ra giá trị 270 < 329
                fingers.append(1) # ngón mở thì append số 1
            else:
                fingers.append(0) # ngón đóng thì append số 0
        print(fingers)
        soNgonTay = fingers.count(1) # đếm xem có bao nhiêu số 1

        h, w,c = lst2[soNgonTay-1].shape
        frame[0:h,0:w] = lst2[soNgonTay-1]

        # vẽ hình hiển thị
        cv2.rectangle(frame,(0,200),(150,400),(0,255,0),-1)
        cv2.putText(frame,str(soNgonTay),(30,390),cv2.FONT_HERSHEY_PLAIN,10,(0,0,0),5)

    # Tính FPS
    cTime = time.time()
    fps = 1/(cTime - pTime) 
    pTime =  cTime
    print(type(fps))
    cv2.putText(frame,f"FPS:{int(fps)}",(150,70),cv2.FONT_HERSHEY_PLAIN,3,(0,0,0),5)
    
    cv2.imshow("Khung hinh ^.^ " , frame)

    if (cv2.waitKey(1) == ord('l')):
        break
cap.release() # giải phóng camera
cv2.destroyAllWindows()#  thoát tất cả các cửa sổ

