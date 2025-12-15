
# Object Detection in Public Places using AirSim & YOLOv8

## Overview
This project demonstrates **real-time aerial object detection and surveillance** in public spaces using the **Microsoft AirSim simulator** and the **YOLOv8 deep learning model**.

A **multirotor drone** is manually flown in a simulated city environment. The drone’s live camera feed is streamed to Python, where **YOLOv8 detects and localizes objects** such as pedestrians, vehicles, and commuters in real time.

---

## Features
- Real-time object detection from aerial view  
- Manual drone patrol using keyboard controls  
- YOLOv8-based detection with confidence scores  
- Bounding box visualization on live video feed  
- Public-place surveillance simulation  
- AirSim–Python API integration  

---

## Requirements

### Software
- Windows 10 / 11 (Recommended)
- Microsoft AirSim (CityEnviron)
- Python 3.8 / 3.9 / 3.10
- Keyboard for manual control

### Python Libraries
```bash
pip install numpy opencv-python ultralytics
pip install airsim
```

---

## Step-by-Step Execution Guide

### Step 1: Download AirSim
1. Visit: https://github.com/microsoft/AirSim/releases  
2. Download **CityEnviron.zip**  
3. Extract (recommended path: `D:\CityEnviron`)  
4. Run `CityEnviron.exe` once

---

### Step 2: Configure AirSim
Edit the file:
```
Documents/AirSim/settings.json
```

Paste the following:
```json
{
  "SettingsVersion": 1.2,
  "SimMode": "Multirotor",
  "ClockSpeed": 1,
  "Vehicles": {
    "Drone1": {
      "VehicleType": "SimpleFlight",
      "AutoCreate": true,
      "AllowAPIAlways": true,
      "Cameras": {
        "front_center": {
          "CaptureSettings": [
            {
              "ImageType": 0,
              "Width": 640,
              "Height": 640,
              "FOV_Degrees": 90
            }
          ],
          "X": 0.5,
          "Y": 0,
          "Z": 0,
          "Pitch": -30,
          "Roll": 0,
          "Yaw": 0
        }
      }
    }
  }
}
```

Restart `CityEnviron.exe` and select **Multirotor**.

---

### Step 3: Run Detection
```bash
python detect.py
```

**Output:**
- Drone auto takeoff (5m)
- Live feed window: *Drone Control Center*
- Bounding boxes + confidence scores

---

### Step 4: Manual Controls
> Click on the video window to enable controls.

| Key | Action |
|---|---|
| W / S | Forward / Backward |
| A / D | Left / Right |
| Q / E | Rotate |
| Z / X | Up / Down |
| ESC | Land & Exit |

---

## Key Concepts
- YOLOv8 Object Detection  
- Aerial Surveillance  

---

## Notes
- NVIDIA GPU recommended
- Use `yolov8n.pt` for higher FPS
- Window focus required for keyboard input

---