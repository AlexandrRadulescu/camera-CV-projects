# camera-CV-projects
A list of my projects that use OpenCV and mediapipe to manipulate objects on screen.

HOW TO RUN IT:
In order to run the files, you must have python version 3.9 - 3.11 for the mediapipe module.

1. Install Python (one of the versions mentioned above)

If you already have a newer python version installed, create a virtual environment. 
Inside a command prompt:

2. Install Mediapipe, PyautoGUI:
`pip3 install mediapipe pyautogui pycaw`

3. Go inside cmd and run the files:
`cd <FOLDER_WITH_FILES_YOU_DOWNLOADED_FROM_HERE>`
`python <filename>.py`


WHAT EACH FILE DOES:
1. HandtrackingModule.py : Detects the hands and returns the pixels on the screen where the landmarks of the specified point in hand is. This is not runnable, but you need it to run the other programs.
2. VolumeHandControll.py : Lets you controll the volume using your hands. If you run it and seems it doesn't work, try typing inside the cmd the number 0. That is the default sound output device.
3. Virtual Drag And Drop.py : Lets you manipulate squares on screen. At first they look like lines because the squares are dynamically and randomly put on screen. To lock in one, simply click your index with your middle finger and to release it just move them away.
4. Mouse_controll.py : Lets you use your hand as a mouse. In order to click, you have to click your thumb with your index. To scroll up, you have to hold your fist, and to scroll down, after holding your fist, put your index and your middle finger up. If it doesnt work, please move a bit back because it reacts at a distance from the camera.  
