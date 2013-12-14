import cv2


class Looper:
    def __init__(self, filename):
        self.filename = filename
        self.cap = cv2.VideoCapture(filename)
        _, self.bgframe = self.cap.read()

    def get(self, attr):
        return self.cap.get(attr)

    def next(self):
        ok, frame = self.cap.read()

        if not ok:
            # We assume a failed read means the end of the input.
            self.cap.release()
            self.cap = cv2.VideoCapture(self.filename)
            ok, frame = self.cap.read()

        return frame
