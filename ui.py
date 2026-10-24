import cv2

import config

FONT = cv2.FONT_HERSHEY_SIMPLEX


def draw_header(frame, gesture, finger_count, mode_text):
    width = frame.shape[1]

    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (width, 90), (30, 30, 30), -1)
    cv2.addWeighted(overlay, 0.75, frame, 0.25, 0, frame)

    cv2.putText(frame, f"Gesture: {gesture}", (20, 35),
                FONT, 0.9, (255, 255, 255), 2)
    cv2.putText(frame, f"Fingers: {finger_count}", (20, 75),
                FONT, 0.9, (0, 255, 0), 2)
    cv2.putText(frame, mode_text, (width - 330, 35),
                FONT, 0.8, config.BRUSH_COLOR, 2)
    cv2.putText(frame, "C: Clear   S: Save   Q: Quit", (width - 400, 75),
                FONT, 0.65, (200, 200, 200), 1)


def draw_clear_progress(frame, progress):
    cv2.rectangle(frame, (20, 105), (220, 125), (255, 255, 255), 2)
    cv2.rectangle(frame, (20, 105), (20 + int(200 * progress), 125),
                  (0, 0, 255), -1)
    cv2.putText(frame, "Clearing...", (230, 123), FONT, 0.6, (0, 0, 255), 2)
