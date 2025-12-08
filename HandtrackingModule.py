import cv2 as cv
import mediapipe as mp
import numpy as np
import math

class handDetector():
    def __init__(self,mode = False, maxHands = 2, detectionCon = 0.5, trackCon  = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils
    
    def find_hands(self, img, draw = True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results and self.results.multi_hand_landmarks:
            if draw:
                for handLms in self.results.multi_hand_landmarks:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img
    
    def findPosition(self, img, handNo = 0, draw = True, pad = 10 ):

        lmList = []
        if self.results and self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
        if draw and lmList:
            x_list = [pt[1] for pt in lmList]
            y_list = [pt[2] for pt in lmList]
            top_left = (min(x_list), min(y_list))
            top_left_padded = (top_left[0] - pad, top_left[1] - pad)
            bottom_right = (max(x_list), max(y_list))
            bot_right_padded = (bottom_right[0] + pad, bottom_right[1] + pad)
            cv.rectangle(img, top_left_padded, bot_right_padded, (0,255,0), 3)
        return lmList




class DragRectang():
    
    def __init__(self,posCenter, size=[200,200]):
        self.posCenter = posCenter
        self.size = size
        self.prevPosx = (posCenter[0] - size[0]/2, posCenter[1] - size[1] / 2)
        self.prevPosy = (posCenter[0] + size[0]/2, posCenter[1] - size[1] / 2)
        self.rectPosx = (posCenter[0] - size[0], posCenter[1] - size[1])
        self.rectPosy = (posCenter[0] + size[0], posCenter[1] + size[1])
        self.colorR = (255,0,255)
        self.previous = False

    def find_Idx_Chk_distance(self, lmList):
        check = lmList[12][1:]
        self.x1,self.y1 = check
        self.cursor = lmList[8][1:]
        self.x2,self.y2 = self.cursor
        self.length = math.hypot(self.x2 - self.x1, self.y2 - self.y1)
        return (self.x1,self.y1), (self.x2,self.y2), self.length


    def Clicked(self, length, active=False):
        # Only allow click if not already dragging another
        if self.length < length and not active:
            self.previous = True
            return True
        else:
            self.previous = False
            return False
        
    def update(self, active=False, distance_between_fingers = 30):
        px, py = self.posCenter
        w, h = self.size
        dragging = False
        if px - w/2 < self.cursor[0] < px + w/2 and py - h/2 < self.cursor[1] < py + h/2:
            self.colorR = (200,0,200)
            if self.Clicked(distance_between_fingers, active):
                self.posCenter = [self.cursor[0], self.cursor[1]]
                self.rectPosx = (int(self.posCenter[0] - w/2), int(self.posCenter[1] - h/2))
                self.rectPosy = (int(self.posCenter[0] + w/2), int(self.posCenter[1] + h/2))
                self.prevPosx = self.rectPosx
                self.prevPosy = self.rectPosy
                dragging = True
            else:
                self.rectPosx = self.prevPosx
                self.rectPosy = self.prevPosy
        else:
            self.colorR = (255,0,255)
            self.rectPosx = self.prevPosx
            self.rectPosy = self.prevPosy
        return dragging
    
    def drawRectang(self, img):
        pt1 = (int(self.rectPosx[0]), int(self.rectPosx[1]))
        pt2 = (int(self.rectPosy[0]), int(self.rectPosy[1]))
        cv.rectangle(img, pt1, pt2, self.colorR, cv.FILLED)
