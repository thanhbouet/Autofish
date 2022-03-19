import keyboard
import mss
import cv2
import numpy
from time import sleep
import time
import pyautogui


pyautogui.PAUSE = 0  #Set delay

# Size xu ly, size rod
wd = {
    'left': 400,
    'top': 200,
    'width': 200,
    'height': 200
}
rod = {
    'left': 240,
    'top': 200,
    'width': 500,
    'height': 100
}
#Doc anh xu ly 2 dau ! <xanh, hong>
notice = cv2.imread('Lightpurple!.png',cv2.IMREAD_UNCHANGED)
greenotice = cv2.imread('Lightgreen!.png',cv2.IMREAD_UNCHANGED)


print("Nhan 'S' de bat dau cau")
print("Nhan 'Q' de dung` cau.")
keyboard.wait('s') #Block the program until press 'S'

# Quay mh
sct = mss.mss()
# Bien delay 2s, tranh thay doi bat ngo
pre = 0
cout = 0
pre2 = 0
cout2 = 0
# Bien dem thoi gian cau ca
time_start = time.time()

while True: #loop
    time_remain = time.time()
    scr = numpy.array(sct.grab(wd))
    scr_remove = scr[:,:,:3]

    def repairRod():
        global time_start
        pyautogui.press('r')
        cv2.waitKey(2000)
        pyautogui.press('c')
        cv2.waitKey(1500)
        pyautogui.press('o')
        cv2.waitKey(2000)
        pyautogui.press('e')
        cv2.waitKey(1000)
        pyautogui.press('e')
        cv2.waitKey(1000)
        pyautogui.press('n')
        cv2.waitKey(2000)
        pyautogui.press('p')
        cv2.waitKey(3000)
        time_start = time.time()

    def findMonster():
        global pre2
        global cout2,cout,time_start
        result = cv2.matchTemplate(scr_remove, greenotice, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        now = max_val
        if cout2 > 5:
            #print("Fish2 notice best point: ", max_val)
            h = greenotice.shape[0]
            w = greenotice.shape[1]
            if abs(now - pre2) > 0.06:
                # cv2.rectangle(scr, max_loc, (max_loc[0] + w, max_loc[1] + h), (255, 255, 255),2)
                print("fish2 detected! Best point: ",max_val)
                time_start = time.time()
                #x = random.randint(10,60)
                #cv2.waitKey(x)
                pyautogui.press('space')
                cv2.waitKey(8000)
                pyautogui.press('t')
                cv2.waitKey(5000)
                pyautogui.press('p')
                cout2 = 0
                cout = 0
                cv2.waitKey(5000)
                print("Continue")
        pre2 = now
        cout2 = cout2 + 1

    def fishDetect():
        global pre
        global cout,cout2,time_start
        result = cv2.matchTemplate(scr_remove,notice, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        now = max_val  
        if cout > 5:
            #print("Fish1 notice best point: ",max_val)
            h = notice.shape[0]
            w = notice.shape[1]
            if abs(now - pre) > 0.06:
                #cv2.rectangle(scr, max_loc, (max_loc[0] + w, max_loc[1] + h), (255, 255, 255),2)
                print("fish1 detected! Best point: ",max_val)
                time_start = time.time()
                #x = random.randint(10, 60)
                #cv2.waitKey(x)
                pyautogui.press('space')
                cv2.waitKey(8000)
                pyautogui.press('t')
                cv2.waitKey(5000)
                pyautogui.press('p')
                cout = 0
                cout2 =0
                cv2.waitKey(5000)
                print("Continue")
        pre = now
        cout = cout + 1

    fishDetect()
    findMonster()
    if time_remain - time_start > 90:
        repairRod()

    gray_scr = cv2.cvtColor(scr, cv2.COLOR_BGR2GRAY)
    #ret, bwscr = cv2.threshold(gray_scr, 150, 255, cv2.THRESH_BINARY)
    #edges = cv2.Canny(scr,threshold1=100,threshold2=200)
    cv2.imshow('Screen Shot', gray_scr) #Btw
    cv2.waitKey(1)
    sleep(.10)
    if keyboard.is_pressed('q'):
        break
