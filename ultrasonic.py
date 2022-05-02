import RPi.GPIO as GPIO
import time
from tkinter import *
import tkinter.font

GPIO.setmode(GPIO.BCM)

TRIG = 14
ECHO = 15

## GPIO setup ##

GPIO.setup(TRIG, GPIO.OUT)
GPIO.output(TRIG, GPIO.LOW)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(18, GPIO.OUT)
LED = GPIO.PWM(18, 500)
LED.start(0)
time.sleep(0.1)

## this is function work existly as the map function in arduino where we pass in the value x and convert them to a differnt value base on the minimal and maximal input and output. ##
## it return a pwm value in this case ## 
def get_pwm(x, in_min, in_max, out_min, out_max):
    if(x > in_max):
        x = in_max
    if(x < in_min):
        x = in_min
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

## this is the loop of where we measure the distance and lit up the led accordingly ##
while(True):
    
    print ("starting measurment....")
    
    ## according the the guide book we need to send out the wave length of 1 micro second so that is why we do a time.sleep
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)

    ## wait for the echo pin to get a high value that start recording the time
    while GPIO.input(ECHO) == 0: 
        pass
    start = time.time()
    
    ## wait for the echo pin to get a low value an record the final time 
    while GPIO.input(ECHO) == 1: 
        pass
    stop = time.time()
    
    ## since the wave have to travel to and from the surface of an object, the distance is double and the speed of sound is about 300m/s and the time it took to travel is start to stop
    ## so our equation is 2d = 340 x (stop - start) => d = 170 x (stop - start). covert into cm we just add 2 extra zero to 170 and we will get our final equation ##
    distance = ((stop - start) * 17000)
    print ("distance: " + str(distance)+ "cm")
    pwm = get_pwm(distance, 2, 40, 100, 0)
    print ("pwm : " + str(pwm))
    LED.ChangeDutyCycle(pwm)
    
    ## sleep for 0.1s before starting the next measurement ##
    time.sleep(0.1)
   
win.mainloop()