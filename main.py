import cv2

import config
import gesture
import ui
from drawing_canvas import DrawingCanvas
from hand_tracker import HandTracker


def main():
    cap = cv2.VideoCapture(config.CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)

    if not cap.isOpened():
        print("ERROR: Could not open the webcam. Close other apps using it "
              "or change CAMERA_INDEX in config.py.")
        return

    tracker = HandTracker()
    stabilizer = gesture.GestureStabilizer(config.STABLE_FRAMES)
    clear_timer = gesture.HoldTimer(config.CLEAR_HOLD_SECONDS)
    canvas = None

    print("Project started. Press 'q' in the video window to quit.")

    while True:
        success, frame = cap.read()
        if not success:
            print("ERROR: Could not read from the webcam.")
            break

        frame = cv2.flip(frame, 1)
        if canvas is None:
            canvas = DrawingCanvas(frame.shape)

        landmarks = tracker.find_hand(frame)

        finger_count = 0
        if landmarks is not None:
            fingers = gesture.get_fingers_up(landmarks)
            finger_count = gesture.count_fingers(fingers)
            raw_gesture = gesture.recognize_gesture(fingers, landmarks)
        else:
            raw_gesture = gesture.NO_HAND
        gesture_name = stabilizer.update(raw_gesture)

        mode_text = "Mode: Waiting"
        if landmarks is not None and gesture_name == gesture.POINTING:
            h, w, _ = frame.shape
            x, y = int(landmarks[8].x * w), int(landmarks[8].y * h)
            x, y = canvas.draw(x, y)
            cv2.circle(frame, (x, y), 10, config.BRUSH_COLOR, -1)
            mode_text = "Mode: DRAWING"
        else:
            canvas.lift_pen()
            if landmarks is not None:
                mode_text = "Mode: PEN UP"

        clear_progress = clear_timer.update(gesture_name == gesture.OPEN_PALM)
        if clear_progress >= 1.0:
            canvas.clear()
        elif clear_progress > 0:
            ui.draw_clear_progress(frame, clear_progress)

        frame = canvas.overlay_on(frame)
        ui.draw_header(frame, gesture_name, finger_count, mode_text)
        cv2.imshow(config.WINDOW_NAME, frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("c"):
            canvas.clear()
        elif key == ord("s"):
            print(f"Drawing saved as {canvas.save()}")

    tracker.close()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
