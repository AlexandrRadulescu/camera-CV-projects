import cv2 as cv
import numpy as np
import HandtrackingModule as htm
import matplotlib.pyplot as plt
###
capH, capW = (1280,760)

cap = cv.VideoCapture(0)
cap.set(3,capH)
cap.set(4,capW)

detector = htm.handDetector()

coeffs = [ 2.69576949e-03, -9.74375336e-01,  9.82073950e+01]
dist = np.poly1d(coeffs)
i = np.arange(100)

plt.figure()
plt.plot(i,dist(i))
plt.show()


while True:
    success, img = cap.read()
    if success:

        img = detector.find_hands(img)
        lmList = detector.findPosition(img)

        if lmList:
            ## From bottom of index to bottom of hand (idx 5 and 0)

            idx = lmList[5][1:]
            bot = lmList[0][1:]
            length = np.sqrt((idx[0] - bot[0])**2 + (idx[1] - bot[1])**2)

            distance = dist(length)
            """
            cv.putText(img, f'Distance: {distance}' ,(bot[0] + 20, bot[1]), cv.FONT_HERSHEY_PLAIN, 
                       1.5, (0,255,255), 1)
            """

            


        cv.imshow("Img", img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print("[ERROR]: Cannot get any input from camera!")