from numpysocket import NumpySocket
import cv2 as cv
import time 

npSocket = NumpySocket()
npSocket.startServer(9999)
print("starting server and waiting for frames")
# counter = 0
# start_time = time.time()
while True:
    # Capture frame-by-frame
    frame = npSocket.recieve()
    # counter += 1
    cv.imshow('Frame', frame)

    # Press Q on keyboard to  exit
    if cv.waitKey(25) & 0xFF == ord('q'):
        break
# print("fps:",100 / ((time.time()-start_time)))
print("Closing")
npSocket.close()