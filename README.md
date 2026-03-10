# Cam Keyboard

A webcam-based virtual keyboard controlled using hand gestures.

The system tracks the user's hand using MediaPipe and detects a pinch
gesture between the thumb and index finger to simulate key presses.

## Features

- Real-time hand tracking
- Pinch gesture detection
- Virtual QWERTY keyboard
- Click sound feedback
- Visual fingertip tracking
- Dynamic keyboard scaling

## Technologies Used

- Python
- OpenCV
- MediaPipe
- Pynput

## How It Works

1. The webcam captures frames in real time.
2. MediaPipe detects 21 hand landmarks.
3. The distance between thumb and index finger is measured.
4. When a pinch is detected over a key region, that key is typed.

## Installation

Install dependencies:

pip install -r requirements.txt

Run the program:

python cam_keyboard.py

## Controls

Move your index finger over a key.

Pinch your thumb and finger together to press the key.

Press ESC to exit.
