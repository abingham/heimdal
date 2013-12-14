import sys

import cv2

from looper import Looper

frames = Looper(sys.argv[1])

print('fps:', int(frames.get(cv2.cv.CV_CAP_PROP_FPS)))
print('size:',
      int(frames.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),
      int(frames.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))

mog = cv2.BackgroundSubtractorMOG()

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

last_frame = frames.next()
last_fgmask = mog.apply(last_frame)
last_fgmask = cv2.cvtColor(last_fgmask, cv2.COLOR_GRAY2BGR)

while frames.ok():
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame = frames.next()
    fgmask = mog.apply(frame)
    fgmask = cv2.cvtColor(fgmask, cv2.COLOR_GRAY2BGR)

    fgmask = fgmask | last_fgmask

    cv2.imshow('frame', frame & fgmask)
    # out.write(frame)
