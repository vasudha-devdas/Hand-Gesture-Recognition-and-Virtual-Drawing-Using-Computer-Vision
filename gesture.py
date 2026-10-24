import math
import time

import config

OPEN_PALM = "Open Palm"
CLOSED_FIST = "Closed Fist"
THUMBS_UP = "Thumbs Up"
PEACE_SIGN = "Peace Sign"
POINTING = "Pointing (Drawing)"
UNKNOWN = "Unknown"
NO_HAND = "No Hand"


def distance(landmarks, a, b):
    return math.hypot(landmarks[a].x - landmarks[b].x,
                      landmarks[a].y - landmarks[b].y)


def hand_size(landmarks):
    return distance(landmarks, 0, 9)


def get_fingers_up(landmarks):
    fingers = []

    fingers.append(distance(landmarks, 4, 17) > distance(landmarks, 3, 17))

    for tip, pip in zip(config.FINGER_TIPS, config.FINGER_PIPS):
        tip_dist = distance(landmarks, 0, tip)
        pip_dist = distance(landmarks, 0, pip)
        fingers.append(tip_dist > pip_dist * config.FINGER_RATIO)

    return fingers


def count_fingers(fingers):
    return sum(fingers)


def _thumb_points_up(landmarks):
    rise = landmarks[2].y - landmarks[4].y
    in_order = landmarks[4].y < landmarks[3].y < landmarks[2].y
    return in_order and rise > 0.6 * hand_size(landmarks)


def recognize_gesture(fingers, landmarks):
    _thumb, index, middle, ring, pinky = fingers
    four_up = [index, middle, ring, pinky]

    if not any(four_up):
        return THUMBS_UP if _thumb_points_up(landmarks) else CLOSED_FIST

    if all(four_up):
        return OPEN_PALM

    if index and middle and not ring and not pinky:
        return PEACE_SIGN

    if index and not middle and not ring and not pinky:
        return POINTING

    return UNKNOWN


class GestureStabilizer:
    def __init__(self, frames_needed):
        self.frames_needed = frames_needed
        self.stable = NO_HAND
        self.candidate = NO_HAND
        self.count = 0

    def update(self, gesture):
        if gesture == self.stable:
            self.candidate, self.count = gesture, 0
        elif gesture == self.candidate:
            self.count += 1
            if self.count >= self.frames_needed:
                self.stable, self.count = gesture, 0
        else:
            self.candidate, self.count = gesture, 1
        return self.stable


class HoldTimer:
    def __init__(self, seconds):
        self.seconds = seconds
        self.start = None

    def update(self, active):
        if not active:
            self.start = None
            return 0.0

        if self.start is None:
            self.start = time.time()

        progress = min((time.time() - self.start) / self.seconds, 1.0)
        if progress >= 1.0:
            self.start = None
        return progress
