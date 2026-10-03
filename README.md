# 🖐️ Camera CV Projects

A collection of hand-tracking projects built with **OpenCV** and **MediaPipe** that let you control your computer and interact with on-screen objects using nothing but your webcam and your hands.

![Python](https://img.shields.io/badge/Python-3.9%20–%203.11-3776AB?logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?logo=opencv&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0097A7?logo=google&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows&logoColor=white)

---





## 📂 Projects

| File | Description |
|------|-------------|
| `HandtrackingModule.py` | Core module that detects hands and returns the on-screen pixel coordinates of each hand landmark. **Not runnable on its own** — required by all the other scripts. |
| `VolumeHandControll.py` | Control your system volume by changing the distance between your fingers. |
| `Virtual Drag And Drop.py` | Grab, move and release squares on screen with your fingers. |
| `Mouse_controll.py` | Use your hand as a mouse — move, click and scroll with gestures. |

---

## ⚙️ Requirements

- **Python 3.9 – 3.11** (required by MediaPipe)
- A webcam
- **Windows** (volume control relies on `pycaw`, which is Windows-only)

---

## 🚀 Installation

**1. Clone the repository**

```bash
git clone https://github.com/<your-username>/camera-CV-projects.git
cd camera-CV-projects
```

**2. (Recommended) Create a virtual environment**

If you already have a newer Python version installed, create a virtual environment with a supported version:

```bash
py -3.11 -m venv venv
venv\Scripts\activate
```

**3. Install the dependencies**

```bash
pip install mediapipe pyautogui pycaw
```

> OpenCV is installed automatically as a dependency of MediaPipe.

---

## ▶️ Usage

Run any of the projects from the repository folder:

```bash
python VolumeHandControll.py
python Mouse_controll.py
python "Virtual Drag And Drop.py"
```

> Note the quotes around `"Virtual Drag And Drop.py"` — they're needed because the filename contains spaces.

Press `Ctrl + C` in the terminal (or close the window) to stop a program.

---

## ✋ Gesture Guide

### 🔊 Volume Control
- Move your **thumb and index finger** closer together or further apart to lower or raise the volume.

https://github.com/user-attachments/assets/1efc1e7a-7e4d-401c-b24c-d9f2fd782ecf


> **Not working?** Type `0` in the terminal when prompted — that selects the default audio output device.

### 🟦 Virtual Drag and Drop
- **Grab a square:** touch your **index finger** with your **middle finger** while hovering over it.
- **Release it:** move the two fingers apart.

> At first the squares may look like lines — they're generated dynamically and placed randomly on screen.

### 🖱️ Mouse Control
| Action | Gesture |
|--------|---------|
| Move cursor | Move your hand |
| Left click | Touch your **thumb** to your **index finger** |
| Scroll up | Make a **fist** |
| Scroll down | Make a fist, then raise your **index and middle fingers** |



https://github.com/user-attachments/assets/05eb9d23-2603-4b09-a475-1c1fbb8ac961



> **Not responding?** Move a bit further back — tracking works best at a certain distance from the camera.

---



## 🛠️ Built With

- [OpenCV](https://opencv.org/) — video capture and image processing
- [MediaPipe](https://developers.google.com/mediapipe) — real-time hand landmark detection
- [PyAutoGUI](https://pyautogui.readthedocs.io/) — mouse control
- [pycaw](https://github.com/AndreMiras/pycaw) — Windows audio control
