import cv2 as cv
import HandtrackingModule as htm
import numpy as np
import pyautogui as pgui
import ctypes


##
capH, capW = (760,1280)
dispH, dispW = (1080,1920)
step = 2
##

## Initialize The Camera
cap = cv.VideoCapture(0)
cap.set(3,capW)
cap.set(4,capH)

## Always On Top
HWND_TOPMOST = -1
SWP_NOMOVE = 0x0002
SWP_NOSIZE = 0x0001


## Detector from Hands
detector = htm.handDetector(detectionCon=0.9)

## Declaring The Length I Get From My Camera
coeffs = [ 2.69576949e-03, -9.74375336e-01,  9.82073950e+01]
dist = np.poly1d(coeffs)


def EucDist(p1,p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def ScrollHandGesture(pkyTop,idxTop, idxMid, midTop, ringTop, pkyMid, ringMid):
    cv.line(img, pkyTop, ringTop, color=(255,0,0), thickness= 2)
    ## Enter the scroll stage
    backTopFingersDist = EucDist(pkyTop,ringTop)
    backMidFingersDist = EucDist(pkyMid, ringMid)
    idxMidDist = EucDist(idxTop,midTop)
    if backTopFingersDist< 23 and backMidFingersDist < 20:
        if idxMidDist < 17 and idxTop[1] - idxMid[1] > 2:
            pgui.scroll(300)
        elif idxTop[1] - idxMid[1] < -2:
            pgui.scroll(-300)



wasClicked = False
distPrev = 0
while True:
    success, img = cap.read()
    if success:
        img = cv.flip(img,1)
        img = detector.find_hands(img)
        lmList = detector.findPosition(img)
        ## Mode Mouse
        if lmList:
            ## Create Bounding Box Where You Can Move The Mouse
            bot_right_bb = (260,660)
            top_left_bb = (1045,180)
            cv.rectangle(img, top_left_bb, bot_right_bb, (0,0,255), 3)

            ## Your index controlls the mouse when its inside the bounding box
            bot = lmList[0][1:]
            idx = lmList[8][1:]
            thb = lmList[4][1:]
            pkyTop = lmList[20][1:]
            idxMid = lmList[6][1:]
            midTop = lmList[12][1:]
            ringTop = lmList[16][1:]
            pkyMid = lmList[18][1:]
            ringMid = lmList[14][1:]

            cv.line(img, idx, thb, color=(0,255,0), thickness=2)

            ## Distance to the center
            cx = int((idx[0] + thb[0]) / 2)
            cy = int((idx[1] + thb[1]) / 2)

            ## Distance to the center of palm
            cbx = int((bot[0] + idxMid[0]) / 2)
            cby = int((bot[1] + idxMid[1]) / 2)

            if top_left_bb[0] > cbx > bot_right_bb[0] and top_left_bb[1] < cby < bot_right_bb[1]:
                pgui.moveTo(bot[0]*step - 500, bot[1]*step - 400) 
                ScrollHandGesture(pkyTop,idx, idxMid, midTop, ringTop,pkyMid,ringMid)
                length = EucDist(idx,bot)
                distClick = EucDist(idx,thb)

                ## Click
                if distClick < 30 and not wasClicked:
                    pgui.click()
                    wasClicked = True
                    cv.circle(img, (cx,cy), 5, (0, 255, 0), cv.FILLED)
                elif distClick >= 50:
                    wasClicked = False

                distance = dist(length)
                cv.putText(img, f'Distance: {int(distance)}' ,(bot[0] + 20, bot[1]), cv.FONT_HERSHEY_PLAIN, 
                        1.5, (0,255,255), 1)

        cv.namedWindow("Controller using hands!", cv.WINDOW_NORMAL)
        cv.resizeWindow("Controller using hands!", capW, capH)

        cv.imshow("Controller using hands!", img)
        cv.moveWindow("Controller using hands!", 0, 0) 
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print("[ERROR] The camera failed to load image!")