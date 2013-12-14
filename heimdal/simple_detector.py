import sys

import cv2

from .background_subtractor import BGSubtractor
from .looper import Looper


def run(source):
    frames = Looper(source)
    bgsub = BGSubtractor(learning_rate=0.1)

    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame = frames.next()
        fgframe = bgsub(frame)

        cv2.imshow('frame', fgframe)

def parse_args(args):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', '-i',
                        dest='input_file',
                        default=None,
                        help='Input movie file. (Overrides camera-id)')
    parser.add_argument('--camera-id', '-c',
                        dest='camera_id',
                        default=0,
                        type=int,
                        help='ID of camera to use.')

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args(sys.argv)
    source = args.camera_id
    if args.input_file is not None:
        source = args.input_file
    run(source)