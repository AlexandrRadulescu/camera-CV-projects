import cv2 as cv
import time
import HandtrackingModule as htm
import math
from pycaw.pycaw import AudioUtilities


######################################################
camW, camH = 640, 480
eRender = 0  # Output devices
####################################################


cap = cv.VideoCapture(0)
cap.set(3, camW)
cap.set(4, camH)

devices = AudioUtilities.GetAllDevices(eRender)
valid_devices = []\

################################################ - Audio Check For Your Device
## Check What Device You Want To Use:
for idx, device in enumerate(devices):
    name = getattr(device, 'FriendlyName', None)
    if not name:
        continue
    try:
        volume = device.EndpointVolume
        # Try to get the volume range to confirm it's valid
        volume.GetVolumeRange()
        print(f"{len(valid_devices)}: {name}")
        valid_devices.append(device)
    except Exception:
        continue

if not valid_devices:
    print("No valid audio output devices found.")
    exit()
#################################################
## Select Your Device :
selected_index = int(input())
device = valid_devices[selected_index]
print(f"\nUsing device: {device.FriendlyName}")
##

previousTime = 0

detector = htm.handDetector(detectionCon=0.7)
volume = device.EndpointVolume

############################################ - Constants From Variables
minVol, maxVol, stepVol = volume.GetVolumeRange()
currLvl =  volume.GetMasterVolumeLevel()
ctrMin, ctrMax, ctrStep = (30, 100, 0.7) # Modify These As You Want
############################################

while True:
    try:
        success, img = cap.read()
        if not success:
            print("Warning: Failed to read frame from webcam.")
            break

        img = detector.find_hands(img)
        lmList = detector.findPosition(img, draw=False)
        #Thumb tip = 4
        #Index tip = 8
        if len(lmList) != 0 :
            thumb = lmList[4][1:]
            index = lmList[8][1:]
            ax,ay = thumb
            bx, by = index
            cx,cy = int((ax + bx)/2), int((ay + by) / 2)
            cv.circle(img, (cx,cy), 5, (0, 255, 255), cv.FILLED)
            cv.line(img, thumb, index, color=(0,0,255), thickness=2)

            length = math.hypot(bx - ax, by - ay)
            print(length, '\n')

            if length < ctrMin:
                cv.circle(img, (cx,cy), 5, (0, 255, 0), cv.FILLED)
                volume.SetMasterVolumeLevel(minVol, None)
                addVol = minVol
            elif length > ctrMax:
                cv.circle(img, (cx,cy), 5, (255, 0, 0), cv.FILLED)
                volume.SetMasterVolumeLevel(maxVol, None)
                addVol = maxVol
            else:
                perc = (length-ctrMin) * ctrStep / 100
                addVol = int((maxVol - minVol) * perc * stepVol)
                setVol = minVol + addVol + 69
                setVol = max(minVol, min(setVol, maxVol))
                volume.SetMasterVolumeLevel(setVol, None)
                addVol = setVol
            cv.putText(img, f'Volume: {addVol}', (cx + 5, cy + 5),cv.FONT_HERSHEY_PLAIN,
                    2, (255,0,0), 1)

        currentTime = time.time()
        fps = 1/(currentTime - previousTime)
        previousTime = currentTime

        cv.putText(img, f'FPS {int(fps)}', (40,40), cv.FONT_HERSHEY_PLAIN,
                    2, (255,0,0), 2)

        cv.imshow("Img", img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    except Exception as e:
        print("[ERROR] Exception in main loop:")
        break

