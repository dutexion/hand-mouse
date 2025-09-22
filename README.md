# hand-mouse

Control the mouse with hand motion capture

https://github.com/user-attachments/assets/70c5e198-73ad-4f4e-8482-2ace9f635b3a

## Features

- Hand gesture recognition using MediaPipe
- Real-time mouse control with palm center tracking
- Click action triggered by fist gesture
- Visual overlay showing hand landmarks
- Smooth pointer movement with jitter reduction

## Requirements

- Python 3.9+
- Webcam

## How to run?

1. `python3 -m venv venv` // Create Virtual Environment
2. `source venv/bin/activate` // Run Virtual Environment
3. `pip3 install -r requirements.txt` // install dependencies
4. `python3 app.py` // start program

## Controls

- Move hand: Move mouse cursor
- Make fist: Click
- Open palm: Release

## Project Structure

- `app.py` - Main entry point
- `config.py` - Configuration and constants
- `gesture_utils.py` - Gesture recognition utilities
- `hand_tracker.py` - Hand tracking and mouse control
- `overlay_ui.py` - HUD overlay interface
