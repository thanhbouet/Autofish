import keyboard
import mss
import cv2
import numpy
from time import time, sleep
import pyautogui

pyautogui.PAUSE = 0  #Set delay after every function call to ZERO

print("Press 's' to start playing.")
print("Once started press 'q' to quit.")
keyboard.wait('s') #Block the program until press 'S'
left = True
x = 340
y = 850
sct = mss.mss() #Create an video capture
dimensions_left = {
    'left': 290,
    'top': 600,
    'width': 150,
    'height': 250
}

dimensions_right = {
    'left': 520,
    'top': 600,
    'width': 150,
    'height': 250
}

wood_left = cv2.imread('woodleft.jpg')

wood_right = cv2.imread('woodright.jpg')
w = wood_left.shape[1] #Get size of wood left
h = wood_left.shape[0]

fps_time = time()
while True: #loop

    if left: #the first time is true
        scr = numpy.array(sct.grab(dimensions_left)) #take pixel details form left button and save in a array
        wood = wood_left
    else:
        scr = numpy.array(sct.grab(dimensions_right)) #same as above #3D ARRAY
        wood = wood_right

    # Cut off alpha
    scr_remove = scr[:, :, :3] # the first three index from scr 3Darray #Take the interest part.

    result = cv2.matchTemplate(scr_remove, wood, cv2.TM_CCOEFF_NORMED)
    # Compare one object to the source and return matrix of coincidence

    _, max_val, _, max_loc = cv2.minMaxLoc(result) # Take value and location of resutl
    print(f"Max Val: {max_val} Max Loc: {max_loc}")
    src = scr.copy()
    if max_val > .85: # Condition of false
        left = not left #Turn
        if left:
            x = 340
        else:
            x = 600
        cv2.rectangle(scr, max_loc, (max_loc[0] + w, max_loc[1] + h), (0, 255, 255), 2) #Draw rectangle around object (wood)

    cv2.imshow('Screen Shot', scr) #Btw
    cv2.waitKey(1)
    pyautogui.click(x=x, y=y)
    sleep(.10)
    if keyboard.is_pressed('q'):
        break

    print('FPS: {}'.format(1 / (time() - fps_time)))
    fps_time = time()