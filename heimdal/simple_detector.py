import sys

import cv2

from .background_subtractor import BGSubtractor
from .frame_reader import FrameReader
from .writer import Writer


def run(source,
        threshold=200,
        output=None):
    bgsub = BGSubtractor(learning_rate=0.1)

    while source.ok:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame = source.next()
        frame = bgsub(frame)

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        frame[frame<threshold] = 0

        cv2.imshow('frame', frame)
        if output:
            output(frame)

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
    parser.add_argument('--output_file', '-o',
                        dest='output_file',
                        default=None,
                        help='Output file.')
    parser.add_argument('--intensity_threshold', '-I',
                        default=0,
                        dest='intensity_threshold',
                        type=int,
                        help='Minimum intensity for thresholding [0-255].')

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args(sys.argv)
    source = args.camera_id
    if args.input_file is not None:
        source = args.input_file

    try:
        freader = FrameReader(source)

        writer = None
        if args.output_file:
            writer = Writer(
                args.output_file,
                width=int(freader.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),
                height=int(freader.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))

        run(freader,
            threshold=args.intensity_threshold,
            output=writer)

    finally:
        if writer:
            writer.close()
        freader.close()