import sys

import cv2

from .background_subtractor import BGSubtractor
from .frame_reader import FrameReader
from .writer import Writer


def run(source,
        threshold,
        min_blob_area,
        display=False,
        output=None):
    bgsub = BGSubtractor(learning_rate=0.1)

    while source.ok:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        orig_frame = source.next()
        frame = orig_frame
        # frame = cv2.blur(orig_frame, (3, 3))
        frame = bgsub(frame)

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        frame[frame<threshold] = threshold

        contours, hierarchy = cv2.findContours(frame,
                                               cv2.RETR_LIST,
                                               cv2.CHAIN_APPROX_SIMPLE)

        # finding contour with maximum area and store it as best_cnt
        best_cnt = None
        max_area = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > max_area and area > min_blob_area:
                max_area = area
                best_cnt = cnt

        # finding centroids of best_cnt and draw a circle there
        if best_cnt is not None:
            M = cv2.moments(best_cnt)
            cx,cy = int(M['m10'] / M['m00']), int(M['m01'] / M['m00'])
            cv2.circle(orig_frame, (cx, cy), 5, 255, -1)


        if display:
            cv2.imshow('frame', orig_frame)
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
    parser.add_argument('--fourcc',
                        dest='fourcc',
                        default='THEO',
                        help='The "fourcc" code for the output video encoding.')
    parser.add_argument('--output_file', '-o',
                        dest='output_file',
                        default=None,
                        help='Output file.')
    parser.add_argument('--intensity_threshold', '-I',
                        default=0,
                        dest='intensity_threshold',
                        type=int,
                        help='Minimum intensity for thresholding [0-255].')
    parser.add_argument('--display', '-d',
                        dest='display',
                        action='store_true',
                        help='Whether the video should be displayed.')

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
                height=int(freader.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)),
                fourcc=args.fourcc)

        run(freader,
            threshold=args.intensity_threshold,
            min_blob_area=100,
            display=args.display,
            output=writer)

    finally:
        if writer:
            writer.close()
        freader.close()