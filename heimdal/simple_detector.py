import sys

import cv2

from .background_subtractor import BGSubtractor
from .frame_reader import FrameReader
from .writer import Writer


def run(source, output=None):
    bgsub = BGSubtractor(learning_rate=0.1)

    while source.ok:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame = source.next()
        fgframe = bgsub(frame)

        cv2.imshow('frame', fgframe)
        if output:
            output(fgframe)

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

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args(sys.argv)
    source = args.camera_id
    if args.input_file is not None:
        source = args.input_file

    freader = FrameReader(source)

    writer = None
    if args.output_file:
        writer = Writer(
            args.output_file,
            width=int(freader.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),
            height=int(freader.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))

    run(freader, output=writer)

    if writer:
        writer.close()