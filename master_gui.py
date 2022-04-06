import threading
import numpy as np
import cv2 as cv
from PIL import Image, ImageTk
from tkinter import Tk, Frame, Button, BOTH, Label, Scale, Radiobutton, StringVar
from tkinter import font as tkFont
import tkinter as tk

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

        ret0, frame = camera.read()
        image = cvMat2tkImg(frame)
        self.stream_panel = Label(image=image)
        self.stream_panel.image = image
        self.stream_panel.grid(column=0, row=0,columnspan=2)

        # capture and display the first frame
        ret0, frame = camera.read()
        image = cvMat2tkImg(frame)
        self.panel = Label(image=image)
        self.panel.image = image
        self.panel.grid(column=2,row=0,columnspan=2)


        self.stopflag = True
        self.btnStart = Button(text="Start Motion", command=self.startstop)
        self.btnStart['font'] = helv18
        self.btnStart.grid(column=3,row=1,sticky='e')

        self.speed_var = StringVar(value="Speed: 0")
        self.speed_label = Label(textvariable=self.speed_var)
        self.speed_label.grid(column=1,row=1,sticky='e',columnspan=2)

        self.btnStream = Button(text="Start Streaming",command=self.stream_start)
        self.btnStream['font']= helv18
        self.btnStream.grid(column=0,row=1, sticky="w")

        # threading
        self.stopevent = threading.Event()
        self.thread = threading.Thread(target=self.capture, args=())
        self.thread.start()

    def stream_start(self):
        pass

    def startstop(self):        #toggle flag to start and stop
        if self.btnStart.config('text')[-1] == 'Start Motion':
            self.btnStart.config(text='Stop Motion')
        else:
            self.btnStart.config(text='Start Motion')
        self.stopflag = not self.stopflag

    def capture(self):
        while not self.stopevent.is_set():
            if not self.stopflag:
                ret0, frame = camera.read()
                image = cvMat2tkImg(frame)
                self.panel.configure(image=image)
                self.panel.image = image

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