import sys

import cv2

from looper import Looper

frames = Looper(sys.argv[1])

print('fps:', int(frames.get(cv2.cv.CV_CAP_PROP_FPS)))
print('size:',
      int(frames.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),
      int(frames.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))

mog = cv2.BackgroundSubtractorMOG()
frame = frames.next()
fgmask = mog.apply(frame)

# Define the # codec and create VideoWriter object
#fourcc = cv2.cv.CV_FOURCC(*'THEO')
#out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
# fourcc = int(frames.get(cv2.cv.CV_CAP_PROP_FOURCC))
#out = cv2.VideoWriter(
#    'output.ogg',
#    fourcc,
#    20,
#    (int(frames.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),
#     int(frames.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))))

while frames.ok():
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame = frames.next()
    fgmask = mog.apply(frame, fgmask, 0.1)
    fgmask = cv2.cvtColor(fgmask, cv2.COLOR_GRAY2BGR)

    cv2.imshow('frame', fgmask & frame)
    # out.write(frame)
