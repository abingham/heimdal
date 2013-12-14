import operator

import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# build background buffer
bg_buffer = list(map(
    lambda f: cv2.cvtColor(f, cv2.COLOR_RGB2GRAY),
    (f[1] for f in (cap.read() for _ in range(1)))))

bg = reduce(operator.add, bg_buffer)
bg /= len(bg_buffer)

while True:
    ok, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    cv2.imshow('frame', bg - frame)
    # bg_buffer = bg_buffer[1:] + [frame]

cap.release()