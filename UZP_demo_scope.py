import tkinter as tk
import sys
import string
import math
from DrawFunction import DrawFunction as df
from  UniversalZeroPlus import UZP


uzp0 = UZP(SPIspeed = 16000000)

samples = []
samples1 = []
nsamples = 512
ADCNsamples = 512
DACfrequency = 1000
ADCfrequency = 1000
PWMfrequency = 4000

PWMratio = 25
PWMdelta = 1

dports = [uzp0.ADC1, uzp0.ADC2, uzp0.ADC3]    # ADC ports to act as the oscilloscope channnels. You can add the additional ones or just use one
PWMports = [uzp0.PWM17, uzp0.PWM19]


###########################################################################################

#Sine wave modulated by cosinus signal on DAC1 channel frequency 2000Hz 512 samples
#Triangle wave on DAC2 channel frequency 2000Hz 512 samples
#PWM channel on PWM18 channel 25% duty 10kHZ

###########################################################################################
uzp0.DACInit(uzp0.DAC1, obuff = 0, generate = 1)
uzp0.DACInit(uzp0.DAC2, obuff = 0, generate = 1)
for i in range(0, nsamples):
    samples.append(2048 + 1900 * math.cos(i*2*3.14/nsamples) * math.sin(i*32*3.14/nsamples))
    if i < nsamples / 2:
        samples1.append(100 + i * 3900 / (nsamples / 2))
    else:
        samples1.append(4000 - (i - nsamples / 2)  * 3900 / (nsamples / 2))

uzp0.DACGenerate(uzp0.DAC1, nsamples, samples, frequency = DACfrequency)
uzp0.DACGenerate(uzp0.DAC2, nsamples, samples1, frequency = 2 * DACfrequency)
uzp0.DACStart(uzp0.DAC1)
uzp0.DACStart(uzp0.DAC2)

uzp0.PWMInit(PWMports)
uzp0.PWMFrequencyDuty(PWMports, frequency = PWMfrequency, duty = PWMratio)
uzp0.PWMStart(PWMports)

###########################################################################################
#End DAC & PWM section
###########################################################################################


###########################################################################################

#ADC initialisartion

###########################################################################################

uzp0.ADCInit(dports, speed = 4)
uzp0.ADCReadVref()
print("Voltage reference = {0:2.2f}".format(uzp0.Vref))

###########################################################################################
#Display initialisation
###########################################################################################
win = tk.Tk()
win.title("30 lines of code oscilloscope :)")
win.resizable(False, False)
canv = tk.Canvas(win, bg="white", height=600, width=1200)
canv.pack()
canv.update()
Drawing = df(win, canv)
canv.update()


###########################################################################################

#Data aquision & oscillogram draw

###########################################################################################

try:
    while True:
        functions = []
        results = []

        ###########################################################################################
        #Data aquision
        ###########################################################################################
        data = uzp0.ADCReadData(dports, nsamples = ADCNsamples, frequency = ADCfrequency)
        #data conversion for function draw class
        for  dport in dports:
            functions.append(Drawing.Convert(data, ADCfrequency, dport))

        #oscillogram draw
        PWMratio += PWMdelta
        if PWMratio > 75 or PWMratio < 25:
            PWMdelta = -PWMdelta
        uzp0.PWMDuty(PWMports, PWMratio)
        Drawing.DrawGrid(functions, xgrid = 10) 
        Drawing.DrawFunctions(functions)
        canv.update()
except:
    print(uzp0.counter)
    uzp0.DACStop(uzp0.DAC1)
    uzp0.DACStop(uzp0.DAC2)

win.mainloop()