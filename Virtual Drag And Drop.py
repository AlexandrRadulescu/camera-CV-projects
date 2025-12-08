import cv2 as cv
import HandtrackingModule as htm
import numpy as np
from random import uniform


#############################
capW, capH = (1280,720)
#############################

cap = cv.VideoCapture(0)
cap.set(3, capW)
cap.set(4, capH)

detector = htm.handDetector(detectionCon=0.8, maxHands = 1)

## Initialize 
print("How many rectangles do you want? \n")
n = input()
print("OK, processing {} elements".format(int(n)))

R = []
for i in range(int(n)):
    val = uniform(0, min(capH,capW) - 200)
    R.append(htm.DragRectang([val, val]))



colorR = (255,0,255)
active_drag = None
while True:
    try:
        success, img = cap.read()
        if not success:
            print("Warning: Failed to read frame from webcam.")
            break
        img = cv.flip(img, 1)
        img = detector.find_hands(img)
        lmList = detector.findPosition(img, draw=False)

        dragging = [False] * int(n)
        
        if lmList:
            for rect in R:
                rect.find_Idx_Chk_distance(lmList)
            for i, rect in enumerate(R):
                # Only allow one to be active at a time
                if active_drag is None or active_drag == i:
                    dragging[i] = rect.update(active=(active_drag is not None and active_drag != i), distance_between_fingers=25)
                else:
                    dragging[i] = False
            # Set which rectangle is being dragged
            if any(dragging):
                active_drag = int(np.argmax(dragging))
            else:
                active_drag = None

        for rect in R:
            rect.drawRectang(img)

        cv.imshow("Virtual Drag And Drop", img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    except Exception as e:
        print("[ERROR] Exception in main loop:", e)
        break