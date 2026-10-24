# Real-Time Hand Gesture Recognition and Virtual Drawing System

## Requirements
- Python 3.9 or newer, 64-bit (works with Python 3.14)
- Internet connection on the FIRST run (downloads the ~8 MB hand model automatically)
- A laptop webcam

## Setup
    python -m venv venv
    venv\Scripts\activate          (Windows)
    source venv/bin/activate       (macOS / Linux)
    pip install -r requirements.txt

## Run
    python main.py

## Controls
- Index finger only  -> draw
- Peace sign         -> pen up (move without drawing)
- Open palm 1.5 sec  -> clear drawing
- Keys: C clear, S save PNG, Q quit

## Files
- main.py           start here
- config.py         settings (colour, brush size, camera index...)
- hand_tracker.py   MediaPipe hand detection
- gesture.py        finger counting + gesture recognition
- drawing_canvas.py virtual drawing board
- ui.py             on-screen panel

## Accuracy features
- Rotation-proof finger detection (uses distances, works with tilted hands)
- Gesture stabiliser (a gesture must be seen 5 frames in a row)
- Adaptive pen smoothing and a jump filter against bad detections
- Frames are shrunk before detection for a higher frame rate
- Tune everything in config.py
