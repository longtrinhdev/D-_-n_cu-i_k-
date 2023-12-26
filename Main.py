from tkinter import*
from tkinter import messagebox
import cv2
import time
import os
import webbrowser
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
import mediapipe as mp
import hand as htm
import math
import keyboard
from ctypes import cast , POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities , IAudioEndpointVolume
import numpy as np
from tkinter import Tk, Button, filedialog
from urllib.parse import urlparse
#1. Hàm nhận diện số đếm qua bàn tay
def Nhandienso():
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
            if (lmList[finger_id[0]][1] < lmList[finger_id[0]-1][1]): #[1,569,270] [0,584,329] lấy ra giá trị 569 < 584
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
        else:
            messagebox.showinfo("Thông báo","Không tìm thấy bàn tay hoặc không phải bàn tay!")
        
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

#2.hàm điều chỉnh thanh âm lượng bằng tay
def Dieuchinhamluong():
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
        else:
            messagebox.showinfo("Thông báo","Không tìm thấy bàn tay hoặc không phải bàn tay!")

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

#3. Hàm tạo phím tắt
def PhimTat():
    # tiến hành tạo giá trị  
    ns= 0
    n = phimTat.get()
    entry_vars = []
    if(n.isdigit()):
        ns =int(n) 
    else:    messagebox.showinfo("Thông báo","Không nhập kí tự!")
    
    Label(win, text='Nhập số lượng phím tắt:').place(x=100, y=400)
    Entry(win, width=20, textvariable=phimTat).place(x=250, y=400)

    y = 430 
    # Tạo phím tắt
    for i in range(0,ns):
        Label(win, text='Tạo phím tắt {}:'.format(i+1)).place(x=100, y=y)
        Entry(win, width=20, textvariable=ds_bien_phimtat[i]).place(x=250, y=y)
        entry_vars.append(ds_bien_phimtat[i].get())
        y+=30
    print(entry_vars)
    return entry_vars
# hàm kiểm tra đường dẫn họp lệ
def is_url(input_data):
    try:
        result = urlparse(input_data)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
def is_path(input_data):
    return os.path.exists(input_data)

def phim_Tat():
    entry_var = PhimTat()
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
    drive_opened = False
    drive_opened_1 = False
    while(True):
        ret, frame = cap.read()
        frame = detector.findHands(frame)
        lmList = detector.findPosition(frame,draw=False)
        # THAO TÁC COI NGÓN TAY 
        if len(lmList)!= 0:
            fingers = []
            #1.Viết cho ngón cái(điểm 4 nằm trái hay phải điểm 3)
            if (lmList[finger_id[0]][1] < lmList[finger_id[0]-1][1]): 
                fingers.append(1) # ngón mở thì append số 1
            else:
                fingers.append(0) # ngón đóng thì append số 0

            #2.Viết cho trường hợp 4 ngón dài trước vì 4 ngón dài ngập xuống được
            for i in range(1,5):
                if (lmList[finger_id[i]][2] < lmList[finger_id[i]-2][2]): 
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

            # tạo phím tắt 1,2,3
            
            if (len(entry_var)==1):
                if (soNgonTay == 1 and not drive_opened):
                    drive_url = entry_var[0]
                    if (is_url(drive_url)):
                        webbrowser.open(drive_url)
                        drive_opened = True
                    else:
                        print("Đường dẫn không hợp lệ!")
            if (len(entry_var) == 2): # 2 phím tắt
                if (soNgonTay == 1 and not drive_opened):
                    drive_url = entry_var[0]
                    if (is_url(drive_url)):
                        webbrowser.open(drive_url)
                        drive_opened = True
                    else:
                        print("Đường dẫn không hợp lệ!")    
                if (soNgonTay == 3):
                    folderPath = entry_var[1] # trùng với file folder gốc
                    if (is_path(folderPath)):
                        os.startfile(folderPath)
                    else:
                        print("Đường dẫn không hợp lệ")
            if (len(entry_var) == 3):
                if (soNgonTay == 1 and not drive_opened):
                    drive_url = entry_var[0] #link web
                    if (is_url(drive_url)):
                        webbrowser.open(drive_url)
                        drive_opened = True
                    else:
                        print("Đường dẫn không hợp lệ")
                if (soNgonTay == 2):
                    folderPath1 = entry_var[1] # link máy
                    if (is_path(folderPath1)):
                        os.startfile(folderPath1)
                    else:
                        print("Đường dẫn không hợp lệ")
                if(soNgonTay == 3):
                    folderPath2 = entry_var[2] # link máy
                    if (is_path(folderPath2)):
                        os.startfile(folderPath2)
                    else:
                        print("Đường dẫn không hợp lệ")
            if (len(entry_var) == 4):
                if (soNgonTay == 1 and not drive_opened):
                    drive_url = entry_var[0] #link web
                    if (is_url(drive_url)):
                        webbrowser.open(drive_url)
                        drive_opened = True
                    else:
                        print("Đường dẫn không hợp lệ")
                if (soNgonTay == 2):
                    folderPath1 = entry_var[1] # link máy
                    if (is_path(folderPath1)):
                        os.startfile(folderPath1)
                    else:
                        print("Đường dẫn không hợp lệ")
                if(soNgonTay == 3):
                    folderPath2 = entry_var[2] # link máy
                    if (is_path(folderPath2)):
                        os.startfile(folderPath2)
                    else:
                        print("Đường dẫn không hợp lệ")
                if (soNgonTay == 4 and not drive_opened_1):
                    drive_url1 =entry_var[3] # link web youtube
                    if (is_url(drive_url1)):
                        webbrowser.open(drive_url1)
                        drive_opened_1 = True
                    else:
                        print("Đường dẫn không hợp lệ")
            if (len(entry_var) == 5):
                if (soNgonTay == 1 and not drive_opened):
                    drive_url = entry_var[0] #link web
                    if (is_url(drive_url)):
                        webbrowser.open(drive_url)
                        drive_opened = True
                    else:
                        print("Đường dẫn không hợp lệ")
                if (soNgonTay == 2):
                    folderPath = entry_var[1] # link máy
                    if (is_path(folderPath)):
                        os.startfile(folderPath)
                    else:
                        print("Đường dẫn không hợp lệ")
                if(soNgonTay == 3):
                    folderPath1 = entry_var[2] # link máy
                    if (is_path(folderPath1)):
                        os.startfile(folderPath1)
                    else:
                        print("Đường dẫn không hợp lệ")
                if (soNgonTay == 4 and not drive_opened_1):
                    drive_url =entry_var[3] # link web youtube
                    if (is_url(drive_url)):
                        webbrowser.open(drive_url)
                        drive_opened_1 = True
                    else:
                        print("Đường dẫn không hợp lệ")
                if (soNgonTay == 5):
                    folderPath2 = entry_var[4]
                    keyboard.press_and_release(folderPath2)
        else:
            messagebox.showinfo("Thông báo","Không tìm thấy bàn tay hoặc không phải bàn tay!")
        # Viết ra FPS
        cTime = time.time() 
        fps = 1/(cTime - pTime) 
        pTime =  cTime 
        # show fps trên màn hình
        print(type(fps))
        cv2.putText(frame,f"FPS:{int(fps)}",(150,70),cv2.FONT_HERSHEY_PLAIN,3,(0,0,0),5)
        
        #3. Xử lý thao tác với ngón tay
        cv2.imshow("Khung hinh ^.^ " , frame)

        if (cv2.waitKey(1) == ord('l')):
            break    
    cap.release() # giải phóng camera
    cv2.destroyAllWindows()#  thoát tất cả các cửa sổ
        
#4. Xuất File    
def Luu_File():
    ds_pt = []
    ds = PhimTat()
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w') as file:
            for i in range(len(ds)):
                file.write('Phím ' + str(i+1)+ ': ' + ds[i]+'\n')
        messagebox.showinfo("Xuất file","Xuất file thành công")
    return ds_pt
#5. Hàm hiển thị trên Listbox

win = Tk()
phimTat = StringVar()
phimTat1 = StringVar()
phimTat2 = StringVar()
phimTat3 = StringVar()
phimTat4 = StringVar()
phimTat5 = StringVar()
ds_bien_phimtat = [phimTat1,phimTat2, phimTat3, phimTat4, phimTat5]
win.title('Ứng dụng nhận diện và thao tác co bản với bàn tay')
win.minsize(height=600,width=500)
Label(win,text="Ứng dụng nhận diện và thao tác cơ bản với bàn tay",fg='red',font=('cambria',15),width=40).grid(row=0)
listbox = Listbox(win, width=80,height=20)
listbox.grid(row=1,columnspan=2)


# tạo các button
button = Frame(win)
Button(button,text='Nhận diện số',command=Nhandienso).pack(side=LEFT)
Button(button,text='Điều chỉnh thanh âm lượng', command= Dieuchinhamluong).pack(side=LEFT)
Button(button,text='Tạo phím tắt',command=PhimTat).pack(side=LEFT)
Button(button,text='Run',command=phim_Tat).pack(side=LEFT)
Button(button,text='Lưu file',command=Luu_File).pack(side=LEFT)
Button(button,text='Thoát',command=win.quit).pack(side=LEFT)
button.grid(row=5,column=0)


win.mainloop()