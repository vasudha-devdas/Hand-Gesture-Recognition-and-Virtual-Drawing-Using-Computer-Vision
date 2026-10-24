# Real-Time Hand Gesture Recognition and Virtual Drawing System

MCA Semester 1 Project Guide, Report Content and Viva Preparation

## 1. Problem Statement

Traditional input devices such as the keyboard, mouse and touchscreen need physical contact. In situations such as classroom presentations, smart-board teaching, public kiosks and hygiene-sensitive places, touch-free interaction is more convenient. Most gesture-recognition systems need special hardware (depth cameras, gloves, sensors), which makes them costly.

This project builds a **low-cost, touch-free interaction system** that uses only a normal laptop webcam. It recognises hand gestures in real time and lets the user draw in the air using the index finger.

## 2. Objectives

1. Capture live video from the laptop webcam using OpenCV.
2. Detect and track the hand and its 21 landmarks using MediaPipe.
3. Recognise gestures: open palm, closed fist, thumbs up and peace sign.
4. Count the number of raised fingers.
5. Allow virtual drawing by moving the index finger.
6. Provide options to clear the drawing (by gesture and by keyboard).
7. Display the detected gesture and finger count on a clean interface.
8. Keep the code simple, modular and beginner-friendly.

## 3. Project Features

- Real-time hand tracking with a skeleton overlay
- Gesture recognition: Open Palm, Closed Fist, Thumbs Up, Peace Sign, Pointing
- Finger counting from 0 to 5
- Air drawing using only the index finger, with smoothing to reduce hand shake
- Pen-up mode using the peace sign (move without drawing)
- Clear canvas by holding an open palm for about 1.5 seconds (with a progress bar), or by pressing C
- Save drawing as a PNG image by pressing S
- Clean dark information panel showing gesture, finger count and mode
- Works with a normal webcam; no GPU or extra hardware needed
- No model training: it uses MediaPipe's pre-trained hand model

## 4. Gesture and Control Guide

| Gesture | Fingers raised | Action |
| --- | --- | --- |
| Pointing | Index only | Draw on screen |
| Peace sign | Index and middle | Pen up (move without drawing) |
| Open palm | All four fingers | Hold 1.5 seconds to clear drawing |
| Closed fist | None | Detected and displayed |
| Thumbs up | Thumb up, others folded | Detected and displayed |

Keyboard shortcuts: **C** clear, **S** save drawing, **Q** quit.

## 5. Software Requirements and Version Notes

| Software | Recommended version |
| --- | --- |
| Python | 3.9, 3.10, 3.11 or 3.12 (64-bit) |
| MediaPipe | 0.10.14 (pinned) |
| OpenCV (opencv-python) | 4.8 to 4.11 |
| NumPy | below 2.0 |
| Operating system | Windows 10/11, macOS or Linux |
| Editor | VS Code with the Python extension |

**Important version notes**

- **Python 3.13 or newer is not supported** by this MediaPipe version. If you have it, install Python 3.11 or 3.12 alongside it and use that for this project.
- The code uses `mp.solutions.hands`, the classic and simplest MediaPipe API. Newer MediaPipe releases have been moving away from it, which is why `requirements.txt` pins version 0.10.14. Do not upgrade MediaPipe in this project.
- NumPy 2.x can break this MediaPipe version, so it is limited to below 2.0.
- Check your Python with `python --version`. On Windows you may need `py -3.11` instead of `python`.

## 6. Installation Commands

Open a terminal in the project folder and run:

```
python -m venv venv
```

Activate the environment:

```
venv\Scripts\activate          (Windows, Command Prompt or VS Code terminal)
source venv/bin/activate       (macOS / Linux)
```

Install the libraries:

```
pip install -r requirements.txt
```

Or install them manually:

```
pip install mediapipe==0.10.14 "opencv-python>=4.8,<4.12" "numpy<2"
```

If PowerShell blocks activation on Windows, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, or simply use the Command Prompt terminal in VS Code.

## 7. Step-by-Step: Running in VS Code

1. Install Python 3.9 to 3.12 from python.org (tick **Add Python to PATH** during installation).
2. Install VS Code and then the **Python** extension by Microsoft.
3. Create a folder named `hand_gesture_drawing` and place `main.py` and `requirements.txt` inside it.
4. In VS Code choose **File > Open Folder** and select that folder.
5. Open a terminal with **Terminal > New Terminal**.
6. Create and activate the virtual environment (Section 6).
7. Press **Ctrl+Shift+P**, choose **Python: Select Interpreter**, and pick the one inside `venv`.
8. Run `pip install -r requirements.txt`.
9. Open `main.py` and click the **Run** button, or type `python main.py` in the terminal.
10. Allow camera permission if asked. The video window opens.
11. Show your hand about 40 to 60 cm from the camera in good lighting, with the palm facing the camera and fingers pointing up.
12. Press **Q** to exit.

## 8. How the Code Works (Simple Explanation)

**Step 1: Capture video.** `cv2.VideoCapture(0)` opens the webcam. A loop reads one frame at a time, which gives the real-time effect. Each frame is flipped (`cv2.flip`) so it works like a mirror.

**Step 2: Detect the hand.** OpenCV frames are in BGR colour order but MediaPipe needs RGB, so the frame is converted with `cv2.cvtColor`. MediaPipe's `Hands` model then finds the hand and returns **21 landmarks** (points such as fingertips and knuckles) with x, y coordinates. Point 8 is the index fingertip, 4 is the thumb tip, and 0 is the wrist.

**Step 3: Find which fingers are up.** The function `get_fingers_up()` compares landmarks:

- For index, middle, ring and pinky: if the fingertip is higher on screen than its middle joint (smaller y value), the finger is up.
- For the thumb: it moves sideways, so the x positions are compared. The left or right hand label from MediaPipe decides the direction.

The result is five True/False values, and counting the True values gives the finger count.

**Step 4: Recognise the gesture.** `recognize_gesture()` applies simple rules to the finger states:

- No fingers up and the thumb pointing upward: Thumbs Up
- No fingers up otherwise: Closed Fist
- All four fingers up: Open Palm
- Index and middle up only: Peace Sign
- Index only: Pointing (drawing mode)

This is rule-based logic on top of a pre-trained detector, so no model training is needed.

**Step 5: Draw in the air.** A black NumPy array of the same size as the frame acts as a **canvas**. In drawing mode, a line is drawn on the canvas from the previous fingertip position to the current one using `cv2.line`. A smoothing formula blends the old and new position to reduce shaking. When the gesture changes, the previous point is reset, which lifts the pen.

**Step 6: Show the drawing.** `merge_canvas()` copies every non-black pixel of the canvas onto the camera frame, so the drawing appears over the live video.

**Step 7: Clear.** Holding an open palm for 1.5 seconds resets the canvas to zeros (black). A red progress bar shows the countdown so the drawing is not cleared by accident. Pressing C does the same instantly.

**Step 8: Display information.** `draw_header()` draws a semi-transparent dark panel with the gesture name, finger count and current mode, using `cv2.putText`.

## 9. Common Errors and Solutions

| Error or problem | Cause | Solution |
| --- | --- | --- |
| `ERROR: Could not open the webcam` | Camera used by another app (Zoom, Teams) or wrong index | Close other apps; change `CAMERA_INDEX` to 1; check camera privacy settings |
| `ModuleNotFoundError: No module named 'cv2'` or `'mediapipe'` | Libraries not installed in the active interpreter | Activate venv, select the correct interpreter in VS Code, run `pip install -r requirements.txt` |
| `Could not find a version that satisfies the requirement mediapipe` | Python 3.13+ or 32-bit Python | Install 64-bit Python 3.11 or 3.12 and recreate the venv |
| `AttributeError: module 'mediapipe' has no attribute 'solutions'` | Newer MediaPipe version installed, or a file named `mediapipe.py` in your folder | `pip install mediapipe==0.10.14`; never name your file `mediapipe.py` or `cv2.py` |
| NumPy error such as `_ARRAY_API not found` | NumPy 2.x installed | `pip install "numpy<2"` |
| Video window opens but is black or very slow | Weak lighting or slow camera | Improve lighting; lower `FRAME_WIDTH` and `FRAME_HEIGHT` to 640 and 480 |
| Hand is not detected | Poor light, too close or too far, busy background | Use even lighting, keep the hand 40 to 60 cm away, use a plain background |
| Wrong gesture detected | Hand tilted or sideways | Keep the hand upright with palm facing the camera |
| Line is shaky | Natural hand movement | Reduce `SMOOTHING` (for example 0.3) for a smoother line |
| PowerShell cannot run `activate` | Execution policy | Use Command Prompt terminal, or `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| Window does not close | Pressed X on the window | Click the video window and press Q |

## 10. Possible Improvements (Future Scope)

- Multiple colours and brush sizes selected by gestures
- Eraser mode
- Controlling the mouse or slide presentations with gestures
- Support for two hands
- Sign language recognition using a trained classifier
- Volume or brightness control using finger distance

---

# MCA Semester 1 Project Report Content

Use the following as the text of your report. Adjust names, dates and guide details to your college format.

## Title Page

**Real-Time Hand Gesture Recognition and Virtual Drawing System**

A project report submitted in partial fulfilment of the requirements for the degree of Master of Computer Applications (MCA), Semester 1.

Submitted by: \[Your Name\], Roll No: \[Number\] Under the guidance of: \[Guide Name\] Department of Computer Applications, \[College / University Name\], \[Academic Year\]

## Certificate, Declaration and Acknowledgement

Add the certificate from your guide and HOD, a declaration that the work is original, and an acknowledgement thanking your guide, faculty, family and friends, as required by your college.

## Abstract

Human-computer interaction is moving from physical devices towards natural, touch-free methods. This project presents a Real-Time Hand Gesture Recognition and Virtual Drawing System developed in Python using OpenCV and MediaPipe. The system captures live video from a standard laptop webcam, detects the hand and its 21 landmarks, determines which fingers are raised, and recognises gestures such as open palm, closed fist, thumbs up and peace sign. It also counts raised fingers and allows the user to draw on the screen in the air by moving the index finger. A clear function is provided through a gesture and a keyboard key. The system uses a pre-trained hand-landmark model, requires no extra hardware and runs in real time on an ordinary laptop. The project demonstrates practical use of computer vision and can be extended to applications such as touch-free presentations, smart classrooms and assistive technology.

## Chapter 1: Introduction

**1.1 Background.** Computer vision allows computers to understand images and video. Gesture recognition is a branch of computer vision where human body movements, especially hand movements, are interpreted as commands.

**1.2 Motivation.** Touch-free interaction is useful for presentations, teaching, public systems and accessibility. Existing solutions often use costly sensors, whereas this project needs only a webcam.

**1.3 Problem Statement.** To design and develop a low-cost, real-time system that recognises hand gestures and supports virtual drawing using only a laptop webcam.

**1.4 Objectives.** As listed in Section 2.

**1.5 Scope.** The system works for one hand, in indoor lighting, with the palm facing the camera. It recognises five gestures and supports drawing in a single colour.

**1.6 Limitations.** Accuracy falls in poor light or with cluttered backgrounds; tilted hands can be misclassified; only one hand is tracked; only predefined gestures are supported.

## Chapter 2: Literature Survey / Technology Overview

**2.1 Existing approaches.** Early gesture recognition used coloured gloves, skin-colour segmentation and contour analysis, which were sensitive to lighting and background. Later approaches used depth sensors such as Kinect and Leap Motion, which need extra hardware. Modern approaches use deep learning to detect hand landmarks directly from an RGB image.

**2.2 Python.** A simple, popular language with strong libraries for image processing and machine learning.

**2.3 OpenCV.** An open-source computer vision library used here to access the webcam, process frames, draw shapes and text, and display the output window.

**2.4 MediaPipe.** An open-source framework by Google offering ready-made machine-learning solutions. Its Hands solution first locates the palm and then predicts 21 three-dimensional landmarks of the hand in real time on a CPU.

**2.5 NumPy.** Used to create and manage the drawing canvas as an array of pixels.

## Chapter 3: System Analysis

**3.1 Existing system.** Mouse, keyboard and touch input need physical contact. Gesture systems with special hardware are expensive.

**3.2 Proposed system.** A software-only gesture system using a webcam, a pre-trained landmark model and simple rules.

**3.3 Feasibility study.** Technical: all libraries are free and run on a normal laptop. Economic: no extra cost. Operational: easy to use, as gestures are natural.

**3.4 Hardware requirements.** Laptop with webcam, minimum 4 GB RAM (8 GB recommended), dual-core processor or better. No GPU needed.

**3.5 Software requirements.** See Section 5.

**3.6 Functional requirements.** Capture video; detect hand; recognise gestures; count fingers; draw; clear; display output.

**3.7 Non-functional requirements.** Real-time response (about 20 to 30 frames per second), usability, portability and reliability.

## Chapter 4: System Design

**4.1 Architecture.** The processing pipeline is:

Webcam, then Frame capture and flip, then BGR to RGB conversion, then MediaPipe hand detection (21 landmarks), then Finger state analysis, then Gesture recognition, then Action (draw, pen up, or clear), then Merge canvas with video and display.

**4.2 Modules.**

1. Video capture module
2. Hand detection and tracking module
3. Finger counting module
4. Gesture recognition module
5. Virtual drawing module
6. Display and user-interface module

**4.3 Algorithm.**

1. Start the webcam.
2. Read a frame and flip it.
3. Convert it to RGB and pass it to MediaPipe.
4. If no hand is found, show "No Hand" and go to step 2.
5. Read the landmarks and check which fingers are up.
6. Count the raised fingers.
7. Identify the gesture using rules.
8. If the gesture is Pointing, draw a line from the previous to the current index fingertip.
9. If the gesture is Open Palm held for 1.5 seconds, clear the canvas.
10. Merge canvas and frame, show information, display the window.
11. If Q is pressed, stop; otherwise repeat from step 2.

**4.4 Diagrams to include.** Use case diagram, data flow diagram (level 0 and level 1), flowchart of the algorithm, and a diagram of the 21 hand landmarks (available in the MediaPipe documentation).

## Chapter 5: Implementation

Explain the code as in Section 8 and include screenshots of each gesture, the finger count, drawing and clearing. Include key code listings (finger detection, gesture recognition and drawing) with explanation.

**Gesture rules table**

| Gesture | Rule |
| --- | --- |
| Open Palm | Index, middle, ring and pinky all up |
| Closed Fist | All four fingers down |
| Thumbs Up | Four fingers down and thumb tip above its joints |
| Peace Sign | Index and middle up; ring and pinky down |
| Pointing | Only index up |

## Chapter 6: Testing

**6.1 Test cases**

| No. | Test | Expected result | Result |
| --- | --- | --- | --- |
| 1 | Start program | Webcam window opens | Pass |
| 2 | Show hand | Skeleton drawn on hand | Pass |
| 3 | Show open palm | "Open Palm", fingers = 5 | Pass |
| 4 | Show fist | "Closed Fist", fingers = 0 | Pass |
| 5 | Show thumbs up | "Thumbs Up", fingers = 1 | Pass |
| 6 | Show peace sign | "Peace Sign", fingers = 2 | Pass |
| 7 | Point with index and move | Line drawn | Pass |
| 8 | Hold open palm 1.5 s | Drawing cleared | Pass |
| 9 | Press C | Drawing cleared | Pass |
| 10 | Press S | PNG image saved | Pass |
| 11 | No hand in view | "No Hand" shown | Pass |
| 12 | Press Q | Program exits | Pass |

Test it yourself and fill the Result column honestly with your own observations. Also note how the system behaves in dim light and with a cluttered background.

## Chapter 7: Results and Discussion

Describe how the system performed: frame rate observed, detection accuracy in good light, and any limitations seen during testing. Add screenshots for each gesture.

## Chapter 8: Conclusion and Future Scope

**Conclusion.** The project achieved real-time hand tracking, gesture recognition, finger counting and air drawing using only a webcam and open-source tools, proving that touch-free interaction is possible at very low cost.

**Future scope.** Multi-colour drawing, eraser, two-hand support, mouse and presentation control, sign-language recognition and a custom trained classifier.

## References

1. MediaPipe Hands documentation, Google (developers.google.com/mediapipe)
2. OpenCV documentation (docs.opencv.org)
3. Python documentation (docs.python.org)
4. NumPy documentation (numpy.org/doc)
5. Zhang et al., "MediaPipe Hands: On-device Real-time Hand Tracking", arXiv:2006.10214, 2020

---

# Viva Questions and Answers

**1. What is your project about?** It is a system that detects a hand through the webcam, recognises gestures like open palm, fist, thumbs up and peace sign, counts raised fingers, and lets the user draw on screen by moving the index finger.

**2. Why did you choose this project?** Touch-free interaction is useful in classrooms, presentations and public places, and I wanted a low-cost solution that needs only a webcam.

**3. What is OpenCV?** OpenCV (Open Source Computer Vision Library) is a library for image and video processing. I used it for webcam access, drawing lines and text, colour conversion and showing the window.

**4. What is MediaPipe?** A Google open-source framework that provides ready-made machine-learning solutions. I used its Hands solution to detect the hand and 21 landmarks.

**5. Did you train a model?** No. MediaPipe provides a pre-trained model. I wrote rule-based logic on the landmark positions to recognise gestures.

**6. What are hand landmarks?** The 21 key points of a hand (wrist, knuckles, joints, fingertips) detected by MediaPipe, each with x, y and z coordinates. For example, 4 is the thumb tip and 8 is the index fingertip.

**7. How do you detect whether a finger is raised?** For four fingers, I compare the y value of the fingertip with its middle joint. If the tip is higher on the screen (smaller y), the finger is up. The thumb is checked using x positions.

**8. Why is the thumb handled differently?** The thumb moves sideways rather than up and down, so comparing y values does not work. Its x position is compared, and the direction depends on whether it is the left or right hand.

**9. Why do you flip the frame?** To create a mirror view so that moving your hand right moves the drawing right, which feels natural.

**10. Why convert BGR to RGB?** OpenCV stores images in BGR order, but MediaPipe expects RGB.

**11. How does the drawing work?** I keep a black NumPy canvas. While the gesture is Pointing, I draw a line from the previous fingertip position to the current one on that canvas. The canvas is then overlaid on the video.

**12. How do you stop drawing when needed?** When the gesture changes (for example to peace sign), the previous point is reset to None, so no line connects the old and new positions. This works like lifting a pen.

**13. How is the drawing cleared?** By holding an open palm for 1.5 seconds or by pressing C. Both reset the canvas to all zeros.

**14. Why a hold time for clearing?** To prevent accidental clearing when the palm appears briefly while changing gestures.

**15. What is the smoothing factor?** It blends the previous and new fingertip positions so the line does not shake. A higher value follows the finger faster; a lower value gives a smoother but slower line.

**16. What is the role of NumPy?** It creates and stores the canvas as an array of pixel values, and OpenCV draws directly on it.

**17. What are min\_detection\_confidence and min\_tracking\_confidence?** Thresholds between 0 and 1. Detection confidence is the minimum certainty to accept a new hand; tracking confidence is the minimum to keep following it between frames. I used 0.7 for both.

**18. What are the limitations?** It works best in good lighting with the hand upright and facing the camera; it tracks one hand; and it has a small set of predefined gestures.

**19. How would you improve it?** Add colours and an eraser, support two hands, control the mouse or slides, and train a custom classifier for more gestures.

**20. What is the difference between detection and recognition?** Detection finds the hand and its landmarks in the image. Recognition decides what gesture the hand is showing.

**21. What is real-time processing?** Processing each frame fast enough (about 20 to 30 frames per second) that the output appears instantly while the user moves.

**22. What are the applications?** Touch-free presentations, smart classrooms, virtual whiteboards, gaming, sign language support, and assistive technology for people who cannot use a mouse.

**23. Why did you use a virtual environment?** It keeps the project's libraries separate from other Python projects and avoids version conflicts.

**24. Why is MediaPipe pinned to version 0.10.14?** The code uses the classic `mp.solutions.hands` API, which this version supports reliably with Python 3.9 to 3.12, and newer releases may change or remove it.

**25. Which Python concepts did you use?** Functions, loops, conditionals, lists, tuples, boolean logic, constants, the `with` statement, modules and f-strings.

Tip for the viva: run the live demo first, show each gesture, then explain the pipeline using the architecture flow in Chapter 4.
