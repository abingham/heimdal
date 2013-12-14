import cv2


class FrameReader:
    def __init__(self, source, loop=True):
        self.source = source
        self.loop = loop
        self.cap = cv2.VideoCapture(source)
        self.ok, self.frame = self.cap.read()

    def close(self):
        self.cap.release()

    def get(self, attr):
        return self.cap.get(attr)

    def next(self):
        frame = self.frame

        self.ok, self.frame = self.cap.read()

        if not self.ok and self.loop:
            # We assume a failed read means the end of the input.
            self.cap.release()
            self.cap = cv2.VideoCapture(self.source)
            self.ok, self.frame = self.cap.read()

        return frame