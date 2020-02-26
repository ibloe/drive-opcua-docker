#!/usr/bin/python
import RPi.GPIO as GPIO
#import pigpio
import time

from __builtin__ import True, False
from pickle import FALSE, TRUE

from random import random
from time import sleep

pin_enable = 4
pout_pwm = 22
pout_direction = 23
pout_enable = 25
max_speed = 9600
min_speed = 200
global current_speed

def init(pin_enable, pout_pwm, pout_direction, pout_enable, min_speed):
    GPIO.setwarnings(False) 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_enable, GPIO.IN)
    GPIO.setup(pout_pwm, GPIO.OUT)
    pwm = GPIO.PWM(pout_pwm, min_speed)
    GPIO.setup(pout_direction, GPIO.OUT)
    GPIO.setup(pout_enable, GPIO.OUT)
    GPIO.output(pout_enable, 0)
    GPIO.output(pout_direction, 0)
    return pwm

def checkSpeed():
    try:
        f = open("/home/pi/opc-ua-server/speed", "r+")
        value = f.readline()
        f.close
        number = int(float(value))
        return number 
    except IOError as e:
        print e.errno
        print e

def checkDirection():
    try:
        f = open("/home/pi/opc-ua-server/moveForward", "r+")
        value = f.read()
        f.close
        if (value == "1"):
            return True
        else:
            return False 
    except IOError as e:
        print e.errno
        print e

def checkEnable():
    enable = GPIO.input(pin_enable)
    if(enable == 1):
        return True
    else:
        return False
    
def ramp(pwm,cur_speed,new_speed):
    if(new_speed>cur_speed):
        #print("speed up from " + str(cur_speed) + " to " + str(new_speed))
        pwm.start(0.5)
        if(cur_speed == 0):
            cur_speed = 200
        for f in range(cur_speed,new_speed,100): #orig: 100
            pwm.ChangeFrequency(f)
            time.sleep(0.05)
        print "    Speed reached"
    elif(cur_speed>new_speed):
        #print("speed down from " + str(cur_speed) + " to " + str(new_speed))
        pwm.start(0.5)
        flag = False
        if(new_speed == 0):
            new_speed = 200
            flag = True
        for f in range(cur_speed,new_speed,-100):
            pwm.ChangeFrequency(f)
            time.sleep(0.05)
        if(flag):
            pwm.stop() 
            print "    Motor stopped"
        else:
            print "    Speed reached"

def state_stop():
    #print "stop"
    global current_speed
    #stop motor
    pwm.stop()
    GPIO.output(pout_enable, 0)
    GPIO.output(pout_direction, 0)
    current_speed = 0
    
    enable = checkEnable()
    forward = checkDirection()
    speed = checkSpeed()
    if(enable):
        GPIO.output(pout_enable, 1)
    if(forward):
        GPIO.output(pout_direction, 1)
    if((enable == True) & (forward == True) & (speed > 0)):
        return state_forward
    elif((enable == True) & (forward == False) & (speed > 0)):
        return state_backward
    return state_stop

def state_forward():
    #print "forward"
    global current_speed
    enable = checkEnable()
    forward = checkDirection()
    speed = checkSpeed()
    #option to stop motor immediate
    #if(enable == False):
    #    current_speed =0
    #    return state_stop
    if((enable == True) & (forward == True) & (speed > 0)):
        if(speed != current_speed):
            print("Forward: Speed change " + str(current_speed) + " to " + str(speed))
            GPIO.output(pout_enable, 1)
            GPIO.output(pout_direction, 1)
            ramp(pwm,current_speed,speed)
            current_speed = speed
            return state_forward
        if(speed == current_speed):
            return state_forward
    print("Ramp to stop " + str(current_speed) + " to " + str(0))
    ramp(pwm,current_speed,0)
    current_speed = 0
    return state_stop  
    
def state_backward():
    #print "backward"
    global current_speed
    enable = checkEnable()
    forward = checkDirection()
    speed = checkSpeed()
    #option to stop motor immediate
    #if(enable == False):
    #    current_speed =0
    #    return state_stop
    if((enable == True) & (forward == False)):
        if(speed != current_speed):
            print("Backward: Speed change " + str(current_speed) + " to " + str(speed))
            GPIO.output(pout_enable, 1)
            GPIO.output(pout_direction, 0)
            ramp(pwm,current_speed,speed)
            current_speed = speed
            return state_backward
        if(speed == current_speed):
            return state_backward
    print("Ramp to stop " + str(current_speed) + " to " + str(0))
    ramp(pwm,current_speed,0)
    current_speed = 0
    return state_stop


state=state_stop

try:
    global current_speed 
    current_speed= 0
    pwm = init(pin_enable,pout_pwm, pout_direction, pout_enable, min_speed)
    pwm.stop()
    print "Start state machine"
    while state: 
        state=state()  # launch state machine
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
    print "Done with states"