import threading
import numpy as np
import cv2 as cv
from PIL import Image, ImageTk
from tkinter import Tk, Frame, Button, BOTH, Label, Scale, Radiobutton, StringVar
from tkinter import font as tkFont
import tkinter as tk

import networking
from numpysocket import NumpySocket
import socket

camera = cv.VideoCapture(0)
width = int(camera.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(camera.get(cv.CAP_PROP_FRAME_HEIGHT))

def cvMat2tkImg(arr):           # Convert OpenCV image Mat to image for display
    rgb = cv.cvtColor(arr, cv.COLOR_BGR2RGB)
    img = Image.fromarray(rgb)
    return ImageTk.PhotoImage(img)

class App(Frame):
    def __init__(self, winname='Car Control'):

        self.root = Tk()

        global helv18
        helv18 = tkFont.Font(family='Helvetica', size=18, weight='bold')

        self.root.wm_title(winname)
        positionRight = int(self.root.winfo_screenwidth() / 3 - width / 2)
        positionDown = int(self.root.winfo_screenheight() / 3 - height / 2)
        # Positions the window in the center of the page.
        self.root.geometry("+{}+{}".format(positionRight, positionDown))
        self.root.wm_protocol("WM_DELETE_WINDOW", self.exitApp)
        Frame.__init__(self, self.root)

        # self.pack(fill=BOTH, expand=1)

        # ret0, frame = camera.read()
        frame = cv.imread("real_sense.jpg")
        frame = cv.resize(frame, (640,480))
        image = cvMat2tkImg(frame)
        self.stream_panel = Label(image=image)
        self.stream_panel.image = image
        self.stream_panel.grid(column=0, row=0,columnspan=2)

        # capture and display the first frame
        # ret0, frame = camera.read()
        frame = cv.imread("steering_wheel.jpg")
        frame = cv.resize(frame, (640,480))
        self.steeringWheel_image = cvMat2tkImg(frame)
        self.panel = Label(image=self.steeringWheel_image)
        self.panel.image = self.steeringWheel_image
        self.panel.grid(column=2,row=0,columnspan=2)


        self.stopflag = True
        self.btnStart = Button(text="Start Motion", command=self.startstop)
        self.btnStart['font'] = helv18
        self.btnStart.grid(column=3,row=1,sticky='e')

        self.btnCommand = Button(text="Connect to Car", command=self.commandSocketSetup)
        self.btnCommand['font'] = helv18
        self.btnCommand.grid(column=2, row=1, sticky='e')
        self.commandSocket = None

        self.speed_var = StringVar(value="Speed: 0")
        self.speed_label = Label(textvariable=self.speed_var)
        self.speed_label.grid(column=1,row=1,sticky='e',columnspan=1)

        self.btnStream = Button(text="Start Stream",command=self.stream_start)
        self.btnStream['font']= helv18
        self.btnStream.grid(column=0,row=1, sticky="w")

        self.stream_sock = None
        self.streaming = False

        # threading
        self.stopevent = threading.Event()

        self.thread = threading.Thread(target=self.capture, args=())
        self.thread.start()
        # self.thread.join()

        self.stream_thread = threading.Thread(target=self.stream_capture, args=())
        self.stream_thread.start()
        # self.stream_thread.join()


    def commandSocketSetup(self):
        if self.commandSocket is None:
            try:
                self.commandSocket = networking.create_car_controller_socket("10.37.0.5",12345)
                self.btnCommand.config(bg='green')
                self.btnCommand.config(text="Close command socket")
            except socket.error:
                self.commandSocket = None
                self.btnCommand.config(bg="red")
        else:
            self.btnCommand.config(text="Connect to Car",bg="")
            self.commandSocket.close()

    def stream_capture(self):
        while not self.stopevent.is_set():
            if self.streaming:
                stream_frame = self.stream_sock.recieve()
                image = cvMat2tkImg(stream_frame)
                self.stream_panel.configure(image=image)
                self.stream_panel.image = image
                # print("streaming")

    def stream_start(self):
        if self.stream_sock is None:
            try:
                self.stream_sock = NumpySocket()
                self.stream_sock.startClient("10.37.0.5", 9999)
                self.btnStream.config(text="Stop Stream")
                self.btnStream.config(bg='green')
                self.streaming = True
                # self.root.update()
            except socket.error:
                self.stream_sock.close()
                self.stream_sock = None
                self.btnStream.config(bg='red')
                print("error connecting to stream")
                # self.root.update()
        else:
            self.btnStream.config(text="Start Stream")
            self.btnStream.config(bg="")
            self.stream_sock.close()
        self.root.update()

    def startstop(self):        #toggle flag to start and stop
        if self.btnStart.config('text')[-1] == 'Start Motion':
            self.btnStart.config(text='Stop Motion')
        else:
            self.btnStart.config(text='Start Motion')
            self.panel.config(image=self.steeringWheel_image)
            self.panel.image = self.steeringWheel_image
        self.stopflag = not self.stopflag

    def capture(self):
        while not self.stopevent.is_set():
            if not self.stopflag:
                frame = cv.cvtColor(camera.read()[-1],cv.COLOR_BGR2GRAY)
                image = cvMat2tkImg(frame)
                self.panel.configure(image=image)
                self.panel.image = image
            else:
                self.panel.configure(image=self.steeringWheel_image)
                self.panel.image = self.steeringWheel_image

    def run(self):  # run main loop
        self.root.mainloop()

    def exitApp(self):  # exit loop
        self.stopevent.set()
        self.root.quit()

app = App()
app.run()
# release the camera
camera.release()
cv.destroyAllWindows()