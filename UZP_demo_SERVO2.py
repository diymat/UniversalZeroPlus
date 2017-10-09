import spidev
from  UniversalZeroPlus import UZP
import string
import sys
import time
import math

uzp0 = UZP(SPIspeed = 8000000)

sleeptime = 0
frequency = 1000
ratio = -100

increment = 0.5


ports = [uzp0.J1, uzp0.J17, uzp0.J10]
ports1 = [uzp0.J14]


try:
    uzp0.SafeMode(1)

    #exponential servo movement curve - slow in the middle fast at the ends
    #for more - please see the https://www.desmos.com/calculator/fegmovpe57
    uzp0.SERVOInit(ports, frequency = 50, exponential = 1)  


    uzp0.SERVOInit(ports1, frequency = 100)

    #time.sleep(5)


    while True:
        while ratio < 0:
            uzp0.SERVOSetPos(ports, ratio)
            uzp0.SERVOSetPos(ports1, ratio)
            ratio += increment
        time.sleep(sleeptime)
        while ratio <= 100:
            uzp0.SERVOSetPos(ports, ratio)
            uzp0.SERVOSetPos(ports1, ratio)
            ratio += increment
        time.sleep(sleeptime)
        while ratio > 0:
            uzp0.SERVOSetPos(ports, ratio)
            uzp0.SERVOSetPos(ports1, ratio)
            ratio -= increment
        time.sleep(sleeptime)
        while ratio > -100:
            uzp0.SERVOSetPos(ports, ratio)
            uzp0.SERVOSetPos(ports1, ratio)
            ratio -= increment
        time.sleep(sleeptime)
    
 
except KeyboardInterrupt:
    print(uzp0.counter)
    exit

