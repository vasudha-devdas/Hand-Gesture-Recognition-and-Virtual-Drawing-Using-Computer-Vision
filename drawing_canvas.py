import math
import time

import cv2
import numpy as np

import config


class DrawingCanvas:
    def __init__(self, frame_shape):
        self.canvas = np.zeros(frame_shape, dtype=np.uint8)
        self.prev_point = None
        self.rejected = 0

    def draw(self, x, y):
        if self.prev_point is None:
            self.prev_point = (x, y)
            return x, y

        px, py = self.prev_point
        move = math.hypot(x - px, y - py)

        if move > config.JUMP_LIMIT:
            self.rejected += 1
            if self.rejected <= config.MAX_REJECTED:
                return self.prev_point
            self.rejected = 0
            self.prev_point = (x, y)
            return x, y
        self.rejected = 0

        speed = (move - config.SPEED_SLOW) / (config.SPEED_FAST - config.SPEED_SLOW)
        speed = max(0.0, min(speed, 1.0))
        alpha = config.SMOOTH_SLOW + (config.SMOOTH_FAST - config.SMOOTH_SLOW) * speed

        x = int(px + (x - px) * alpha)
        y = int(py + (y - py) * alpha)

        cv2.line(self.canvas, self.prev_point, (x, y),
                 config.BRUSH_COLOR, config.BRUSH_SIZE)
        self.prev_point = (x, y)
        return x, y

    def lift_pen(self):
        self.prev_point = None
        self.rejected = 0

    def clear(self):
        self.canvas[:] = 0
        self.lift_pen()

    def overlay_on(self, frame):
        gray = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
        frame[mask > 0] = self.canvas[mask > 0]
        return frame

    def save(self):
        filename = f"drawing_{int(time.time())}.png"
        cv2.imwrite(filename, self.canvas)
        return filename
