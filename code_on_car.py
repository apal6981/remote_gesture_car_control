# python3 ECEnRacer.py
''' 
This program is for ECEN-631 BYU Race
*************** RealSense Package ***************
From the Realsense camera:
	RGB Data
	Depth Data
	Gyroscope Data
	Accelerometer Data
*************** Arduino Package ****************
	Steer(int degree) : -30 (left) to +30 (right) degrees
	Drive(float speed) : -3.0 to 3.0 meters/second
	Zero(int PWM) : Sets front wheels going straight around 1500
	Encoder() : Returns current encoder count.  Reset to zero when stop
	Pid(int flag) : 0 to disable PID control, 1 to enable PID control
	KP(float p) : Proporation control 0 ~ 1.0 : how fast to reach the desired speed.
	KD(float d) : How smoothly to reach the desired speed.

    EXTREMELY IMPORTANT: Read the user manual carefully before operate the car
**************************************
'''

# import the necessary packages
from Arduino import Arduino
# from Realsense_derek import *
# from RealSense import *
import numpy as np
# import imutils
import cv2 as cv
import controller	# For driving and steering
import random
import networking

try:
    print("Init Car")
	# Use $ ls /dev/tty* to find the serial port connected to Arduino
    Car = Arduino("/dev/ttyUSB0", 115200)                # Linux
	#Car = Arduino("/dev/tty.usbserial-2140", 115200)    # Mac

    Car.zero(1500)      # Set car to go straight. Change this for your car.
    Car.pid(1)          # Use PID control
	# You can use kd and kp commands to change KP and KD values.  Default values are good.
	# loop over frames from Realsense
	# print("Driving Car")
	# controller.start_driving(Car)
	# print("Car started")
    counter = 0
    writer = None
    speed = 1
    # Speed 1 values
    k_p = 0.8   # increase until oscillation, then half
    k_d = 0.4   # increase until minimal oscillation


    # create socket to get turn commands
    car_sock = networking.create_car_command_server_socket("10.37.0.5", 12345)
    input_gen = networking.car_input_receive_generator(car_sock) # generator to get info from socket

    start_key = ''
    print("### Press spacebar then enter to start! ###")
    while start_key != ' ':
        start_key = input()

    def string_generator():
        choice = random.randint(0,1)
        if choice == 0:
            sign = random.randint(0,1)
            if sign == True:
                return "SPD_-1.5"
            else:
                return "SPD_001.5"
        else:
            sign = random.randint(0,1)
            if sign == True:
                return "DIR_-020"
            else:
                return "DIR_0020"

    def parse_string(word):
        x = word.split('_')
        control = x[0]
        val = float(x[1])
        return control, val


    for data in input_gen: # keep looping until the socket closes
        counter += 1        

        control, val = parse_string(data)
        if control == 'SPD':
            Car.drive(val)
        if control == 'DIR':
            Car.steer(val)

		
except Exception as e:
	print(e.with_traceback())
    # print(e)

finally:       
    print("Deleting Car")
    if Car is not None:
        Car.drive(0)
        del Car

