from RealSense import *
import cv2 as cv
# import imutils	
from numpysocket import NumpySocket


host_ip = '10.32.120.58'  # change me



rs = None
rs = RealSense("/dev/video2", RS_VGA)    # RS_VGA, RS_720P, or RS_1080P
writer = None
recording = False
frameIndex = 0

npSocket = None
npSocket = NumpySocket()
npSocket.startServer(host_ip, 9999)

while True:
    (frame_time, rgb, depth, accel, gyro) = rs.getData()
    gray = cv.cvtColor(rgb, cv.COLOR_BGR2GRAY)
    resize = cv.resize(gray,(320,240), interpolation = cv.INTER_AREA)
    # print("gray shape",gray.shape)
    npSocket.send(resize)
    # print("sent:",frameIndex)
    frameIndex += 1

    # if writer is None and recording is True:
    #     # initialize our video writer
    #     writer = cv2.VideoWriter('Video.avi', cv2.VideoWriter_fourcc(*'MJPG'), 15, (rgb.shape[1], rgb.shape[0]), True)

    # cv2.imshow("RGB", rgb)
    # cv2.imshow("Depth", depth)
    
    # if recording == True:
    #     # write the output frame to disk
    #     writer.write(rgb)

    # key = cv2.waitKey(1) & 0xFF
    # if key == ord("r"):     # Start Recording
    #     recording = True
    # if key == ord("s"):     # Stop Recording
    #     recording = False
    # if key == ord("i"):     # Save image
    #     filename = "image" + str(frameIndex) + ".jpg"
    #     cv2.imwrite(filename, rgb)
    #     frameIndex += 1
    # if key == ord("q"):
    #     break

if npSocket is not None:
    npSocket.close()
if writer:
    writer.release()
if rs is not None:
    del rs


