import cv2


class BGSubtractor:
    def __init__(self, learning_rate=-1):
        self.mog = cv2.BackgroundSubtractorMOG()
        self.mask = None
        self.learning_rate = learning_rate

    def __call__(self, frame):
        if self.mask is None:
            self.mask = self.mog.apply(frame)
        else:
            self.mask = self.mog.apply(
                frame,
                self.mask,
                self.learning_rate)

        self.mask = cv2.cvtColor(
            self.mask,
            cv2.COLOR_GRAY2BGR)

        return self.mask & frame
