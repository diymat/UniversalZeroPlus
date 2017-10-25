import spidev
import time
import signal
import math

class UZP:
    NOP = 0
    GPIO_INIT = 1
    GPIO_INIT_L = 2 
    GPIO_SET = 3
    GPIO_SET_L = 4
    GPIO_GROUP = 5     
    GPIO_SET_GROUP = 6
    GPIO_READ_GROUP = 7
    GPIO_READ_G = 8
    GPIO_READ = 9
    GPIO_READ_L = 10
    GPIO_TOGGLE = 11
    GPIO_TOGGLE_L = 12
    GPIO_TOGGLE_G = 13

    ADC_INIT_L = 30
    ADC_SET_SAMPLING_L = 31
    ADC_READ = 32
    ADC_READ_L = 33
    ADC_READ_FAST = 34
    ADC_READ_VREF = 35 

    DAC_INIT = 50
    DAC_WRITE = 51
    DAC_PERIOD = 52
    DAC_GENERATE = 53
    DAC_SYNC = 54
    DAC_START = 55
    DAC_STOP = 56

    PWM_INIT_L = 70
    PWM_GROUP = 71
    PWM_SET = 72
    PWM_SET_G = 73
    PWM_FREQ = 74
    PWM_FREQ_DUTY_L = 75
    PWM_FREQ_L = 85
    PWM_FREQ_G = 75
    PWM_DUTY = 76
    PWM_DUTY_L = 77
    PWM_DUTY_G = 78
    PWM_START = 79
    PWM_START_L = 80
    PWM_START_G = 81
    PWM_STOP = 82
    PWM_STOP_L = 83
    PWM_STOP_G = 84

    SERVO_INIT = 100
    SERVO_GROUP = 101
    SERVO_SET = 103
    SERVO_SET_G = 104

    IMPULSE_READ	= 110


    SAFE_MODE = 200



    GPIO_INPUT = 0
    GPIO_OUTPUT = 1

    GPIO_TYPE_PP = 0
    GPIO_TYPE_OD = 1

    GPIO_SPEED_LOW = 0
    GPIO_SPEED_MEDIUM = 1
    GPIO_SPEED_HIGH = 3

    GPIO_PUPD_NO_PP = 0
    GPIO_PUPD_PU = 1
    GPIO_PUPD_PD = 2

    ACK = 0xdf45    
    

#PORTS DEFINITIONS

########################################################################################################################################################
#                                                                       PORTS MAP                                                                      #
########################################################################################################################################################
#GPIO   0 |  1 |  2 |  3 |  4 |  5 |  6 |  7 |  8 |  9 |  10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 |
#ADC      |    |    |  1 |  2 |  3 |  4 |  5 |  6 |  7 |  8  | 9  | 10 | 11 |    |    | 12 | 13 | 14 | 15 |    |    |    |    |    |    |    |    |    |
#DAC      |    |    |    |    |    |    |  1 |  2 |    |     |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
#SERVO    |    |    |  1 |  2 |  3 |  4 |  5 |  6 |  7 |     | 8  | 9  |    | 10 |    |    |    |    | 11 | 12 | 13 |    | 14 | 15 | 16 | 17 | 18 | 19 |
#COMP     |    |    | 7P | 1P | 2M | 2P | 7M | 1M |    |     | 4P |    | 4M | 5M | 6P | 3M | 5P | 3P | 6M |    |    |    |    |    |    |    |    |    |
########################################################################################################################################################
########################################################################################################################################################

    COMP1M = 8
    COMP1P = 4
    COMP2M = 5
    COMP2P = 6
    COMP3M = 16
    COMP3P = 18
    COMP4M = 13
    COMP4P = 11
    COMP5M = 14
    COMP5P = 17
    COMP6M = 19
    COMP6P = 15
    COMP7M = 7
    COMP7P = 3

    DAC1 = 7
    DAC2 = 8

    J1 = 3
    J2 = 4
    J3 = 5
    J4 = 6
    J5 = 7
    J6 = 9
    J7 = 10
    J8 = 11
    J9 = 12
    J10 = 14
    J11 = 19
    J12 = 20
    J13 = 21
    J14 = 23
    J15 = 24
    J16 = 25
    J17 = 26
    J18 = 27
    J19 = 28

    PWM1 = 3
    PWM2 = 4
    PWM3 = 5
    PWM4 = 6
    PWM5 = 7
    PWM6 = 9
    PWM7 = 10
    PWM8 = 11
    PWM9 = 12
    PWM10 = 14
    PWM11 = 19
    PWM12 = 20
    PWM13 = 21
    PWM14 = 23
    PWM15 = 24
    PWM16 = 25
    PWM17 = 26
    PWM18 = 27
    PWM19 = 28

    SERVO1 = 3
    SERVO2 = 4
    SERVO3 = 5
    SERVO4 = 6
    SERVO5 = 7
    SERVO6 = 9
    SERVO7 = 10
    SERVO8 = 11
    SERVO9 = 12
    SERVO10 = 14
    SERVO11 = 19
    SERVO12 = 20
    SERVO13 = 21
    SERVO14 = 23
    SERVO15 = 24
    SERVO16 = 25
    SERVO17 = 26
    SERVO18 = 27
    SERVO19 = 28


    ADC1  = 3
    ADC2  = 4
    ADC3  = 5 
    ADC4  = 6
    ADC5  = 7
    ADC6  = 8
    ADC7  = 9
    ADC8  = 10
    ADC9  = 11
    ADC10 = 12
    ADC11 = 13
    ADC12 = 16
    ADC13 = 17
    ADC14 = 18
    ADC15 = 19


    UZP_RESET = 0b111111

    ADC_CONVTABLE = [ADC1, ADC2, ADC3, ADC4, ADC5, ADC6, ADC7, ADC8, ADC9, ADC10, ADC11, ADC12, ADC13, ADC14, ADC15 ]

    def __init__(self, device=0, port=0, SPIspeed=500000, SPImode=0b00):
        self.spidev = device
        self.spiport = port
        self.speed = SPIspeed
        self.mode = SPImode
        self.spi = spidev.SpiDev()
        self.ConversionResults = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0]]
        self.GPIO_Status = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.DAC = [7, 8]
        self.PWM = [3,4,5,6,7,9,10,11,12,14,19,20,21,23,24,25,26,27,28]
        self.GPIO = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]
        self.DACVref = 2.5
        self.Vref = 3.3
        self.spi.open(device, port)
        self.spi.mode = SPImode
        self.spi.max_speed_hz = SPIspeed
        self.FADC_NSamples = 0
        self.inside = 0
        self.LowPass = [[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
        self.HC_Filter = 0
        self.counter = 0
        self.servo = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
        self.safemode = 0
        self.ADCResolution = 12
        self.DACResolution = 12
        self.w = False;

    def WaitForACK(self):
        if self.safemode != 0:
            self.w = True;
            while self.Read16() != self.ACK:
                continue
            self.w = False

    def CD32(self, val):
        return int(val) | 0x80000000

    def CD16(self, val):
        return int(val) | 0x8000

    def uSeconds(self, microseconds):
        return (int)(microseconds * 1000)


    def mSeconds(self, miliseconds):
        return self.uSeconds(miliseconds * 1000)


    def Send16(self, value):
        self.spi.xfer([(value & 0xff00) >> 8, (value & 0xff)])


    def Send32(self, value):

        self.Send16(value & 0xffff)
        self.Send16(value >> 16)

    def SafeSend16(self, val16):
        s = signal.signal(signal.SIGINT, signal.SIG_IGN)
        self.Send16(val16)
        signal.signal(signal.SIGINT, s)

    def SafeSend1616(self, val16_1, val16_2):
        s = signal.signal(signal.SIGINT, signal.SIG_IGN)
        self.Send16(val16_1)
        self.Send16(val16_2)
        signal.signal(signal.SIGINT, s)

    def SafeSend163216(self, val16_1, val32_2, val16_3):
        s = signal.signal(signal.SIGINT, signal.SIG_IGN)
        self.Send16(val16_1)
        self.Send32(val32_2)
        self.Send16(val16_3)
        signal.signal(signal.SIGINT, s)


    def SafeSend1632(self, val16_1, val32_2):
        s = signal.signal(signal.SIGINT, signal.SIG_IGN)
        self.Send16(val16_1)
        self.Send32(val32_2)
        signal.signal(signal.SIGINT, s)
    
    def SafeSend161632(self, val16_1, val16_2, val32_3):
        s = signal.signal(signal.SIGINT, signal.SIG_IGN)
        self.Send16(val16_1)
        self.Send16(val16_2)
        self.Send32(val32_3)
        signal.signal(signal.SIGINT, s)

    def SafeSend16163232(self, val16_1, val16_2, val32_3, val32_4):
        s = signal.signal(signal.SIGINT, signal.SIG_IGN)
        self.Send16(val16_1)
        self.Send16(val16_2)
        self.Send32(val32_3)
        self.Send32(val32_4)
        signal.signal(signal.SIGINT, s)

    def SafeSend16323216(self, val16_1, val32_2, val32_3, val16_4):
        s = signal.signal(signal.SIGINT, signal.SIG_IGN)
        self.Send16(val16_1)
        self.Send32(val32_2)
        self.Send32(val32_3)
        self.Send16(val16_4)
        signal.signal(signal.SIGINT, s)

    def SafeSend163232(self, val16_1, val32_2, val32_3):
        s = signal.signal(signal.SIGINT, signal.SIG_IGN)
        #print("{0:x} {1:x} {2:x}".format( val16_1, val32_2, val32_3));        
        self.Send16(val16_1)
        self.Send32(val32_2)
        self.Send32(val32_3)
        signal.signal(signal.SIGINT, s)

    def SafeSend163232323216(self, val16_1, val32_2, val32_3, val32_4, val32_5, val16_6):
        s = signal.signal(signal.SIGINT, signal.SIG_IGN)
        self.Send16(val16_1)
        self.Send32(val32_2)
        self.Send32(val32_3)
        self.Send32(val32_4)
        self.Send32(val32_5)
        self.Send16(val16_6)
        signal.signal(signal.SIGINT, s)

    def SafeSend16323232323216(self, val16_1, val32_2, val32_3, val32_4, val32_5, val32_6, val16_7):
        s = signal.signal(signal.SIGINT, signal.SIG_IGN)
        self.Send16(val16_1)
        self.Send32(val32_2)
        self.Send32(val32_3)
        self.Send32(val32_4)
        self.Send32(val32_5)
        self.Send32(val32_6)
        self.Send16(val16_7)
        signal.signal(signal.SIGINT, s)
        

    def Read16(self):

        result16 = 0
        while result16 == 0:
            result = self.spi.readbytes(2)
            result16 = (result[0] * 256) + result[1]
        return result16

            
    def Read32(self):

        nwords = 0
        result16 = 0
        result32 = 0
        while nwords < 2:
            while result16 == 0:
                result = self.spi.readbytes(2)
                result16 = (result[0] * 256) + result[1]
            result32 += (result16 << 16 * (nwords))
            nwords += 1
            result16 = 0
        return result32

        #          1111111111222222222233
        #01234567890123456789012345678901
        #1ppppppppppppppp1ppppppppppppppx

    def CodePortNumbers(self, Ports):

        PortNumbers = (1 | (1 << 16))
        NPorts = 0
        for port in Ports:
            if(port) < 15:
                PortNumbers |= (1 << (port + 1))
            if(port) > 14 and port < 29:
                PortNumbers |= (1 << (port + 2))
            NPorts += 1
        return [PortNumbers, NPorts]

    def SafeMode(self, mode):
        """
        Sets SafeMode 

        Parameters:
            mode -  0 - methods do not send ACK when completed
                    1 - methods send ACK when completed
        """
        self.counter += 1
        if mode != 0:
            mode = int(1)
        self.safemode = mode
        c16 = self.SAFE_MODE | (mode << 8)
        self.SafeSend16(c16)
        self.WaitForACK()

    def GPIOInit(self, Ports, mode=GPIO_INPUT, type=GPIO_TYPE_PP, popd=GPIO_PUPD_NO_PP, speed=GPIO_SPEED_HIGH, state=0):
        """
        Sets up the GPIO 

        Parameters:
            Ports - list of the the port numbers

            mode  - GPIO_INPUT / GPIO_OUTPUT

            type  - GPIO_TYPE_PP - push-pul
                  - GPIO_TYPE_OD - open drain

            popd  - GPIO_PUPD_NO_PP - no push/pull
                  - GPIO_PUPD_PU - pull-up
                  - GPIO_PUPD_PD - pull-down

            speed - GPIO_SPEED_HIGH - port high speed 
                  - GPIO_SPEED_MEDIUM - port medium speed 
                  - GPIO_SPEED_LOW - port low speed 
                  keep the speed high if RPi is not battery operated

            state - initial GPIO level
                    
        """
        self.counter += 1
        CodedPorts = self.CodePortNumbers(Ports)
        if(CodedPorts[1] == 0):
            return
        c16 = ((mode | (type << 1) | (speed << 2) | (popd << 4) | (state << 6)) << 8)
        c16 |= self.GPIO_INIT_L
        self.SafeSend1632(c16, CodedPorts[0])
        self.WaitForACK()

    def GPIOSet(self, Ports, value):
        """
        Sets the GPIO 

        Parameters:
            Ports - list of the the port numbers

            value = 0 or not zero. Sets the GPIO output level to low or high                    
        """
        self.counter += 1
        if(value != 0):
            c16 = 0x100
        else:
            c16 = 0
        if len(ports) == 1:
            c16 |= int(Ports[0]) << 9
            c16 |= self.GPIO_SET
            self.SafeSend16(c16)
        else:
            CodedPorts = self.CodePortNumbers(Ports)
            if(CodedPorts[1] == 0):
                return
            if(CodedPorts[1] > 1):
                c16 |= self.GPIO_SET_L
                self.SafeSend1632(c16, CodedPorts[0])
            else:
                c16 |= self.GPIO_SET
                c16 |= (Ports[0] << 9)
                self.SafeSend16(c16)
        self.WaitForACK()

    def decode32(self, val):
        val = int(val)
        return ((val & 0x7fff0000) >> 1) + (val & 0x7fff);


    def GPIOToggle(self, Ports):
        """
        Toggles the GPIO ports

        Parameters:
            Ports - list of the the port numbers
        """

        self.counter += 1
        CodedPorts = self.CodePortNumbers(Ports)
        if(CodedPorts[1] == 0):
            return 
        if(CodedPorts[1] > 1):
            c16 = self.GPIO_TOGGLE_L
            self.SafeSend1632(c16, CodedPorts[0])
        else:
            c16 = self.GPIO_TOGGLE
            c16 |= (Ports[0] << 9)
            self.SafeSend16(c16)            
        self.WaitForACK()

    def GPIORead(self, Ports):
        """
        Reads the input GPIO ports

        Parameters:
            Ports - list of the the port numbers

            returns the list of the read values on the coresponding positions in the list (GPIO19 is on the 19 position on the list)                   
        """

        self.counter += 1
        result = 0
        CodedPorts = self.CodePortNumbers(Ports)
        if(CodedPorts[1] == 0):
            return []
        c16 = self.GPIO_READ_L
        self.SafeSend1632(c16, CodedPorts[0])

        result = self.Read32()
        self.WaitForACK()
        tmp = result & 0b01111111111111100000000000000000
        tmp = tmp >> 2
        result = ((result & 0xffff) >> 1) | tmp
        
        ports = []
        for port in range(0,29):
            if (result & (1 << port)) != 0:
                ports.append(1)
            else:
                ports.append(0)
        return ports

    
    def DACInit(self, Port, obuff=1, generate=0, initialVoltage=0):
        """
        Initialises the DAC Port

        Parameters:
            Port - DAC port number

            obuff - output buffer on/off
            generate - init in the generator mode
            initalVoltage - initial voltage in the raw format(0-4095) 
        """

        self.counter += 1
        if(Port != self.DAC1 and Port != self.DAC2):
            return
        
        c16 = self.DAC_INIT
        c16 = c16 + (((obuff) | (generate << 1) | (Port << 2)) << 8)

        self.SafeSend1616(c16, int(initialVoltage) | 0xf000)
        self.WaitForACK()
        
 
    def DACWrite(self, Port, Voltage):
        """
        Sets the DAC Port voltage 

        Parameters:
            Port - DAC port number
            Voltage - initial voltage in the raw format(0-4095) 
        """

        self.counter += 1
        if(Port != self.DAC1 and Port != self.DAC2):
            return
        
        c16 = self.DAC_WRITE
        c16 += (Port << 2) * 0x100
        
        self.SafeSend1616(c16, int(initialVoltage) | 0xf000)
        self.WaitForACK()
 
    def DACGenerate(self, Port, nsamples, samples, frequency, period=0):
        """
        Initialises the DAC Waveform generator. Does not start the generation

        Parameters:
            Port - DAC port number
            nsamples - number of samples (1 - 4096)
            samples - list with the samples (number of the samples must be equal to nsamples value)
            frequency - frequency of the generated signal in Hz
            period - period of the generated signal in ns
        """

        self.counter += 1
        if(Port != self.DAC1 and Port != self.DAC2):
            return
        if(period == 0 and frequency == 0.0):
            return
        if(nsamples != len(samples)):
            return
        
        c16 = self.DAC_GENERATE
        c16 += (Port << 2) * 0x100

        if(period == 0):
            period = int(1e9 / frequency)
        s = signal.signal(signal.SIGINT, signal.SIG_IGN)
        self.Send16(c16)
        self.Send16(nsamples)
        self.Send32(period | 0x80000000)
        for i in range(0, nsamples):
            self.Send16(int(samples[i]) | 0x8000)
        signal.signal(signal.SIGINT, s)
        self.WaitForACK()

    def DACFrequency(self, Port, frequency=0.0, period=0):
        """
        Sets the DAC port generator signal frequency. If the generation was started it will change the frequency on the fly

        Parameters:
            Port - DAC port number
            frequency - frequency of the generated signal in Hz
            period - period of the generated signal in ns
        """

        self.counter += 1
        if(Port != self.DAC1 and Port != self.DAC2):
            return
        if(period == 0 and frequency == 0.0):
            return
        
        c16 = self.DAC_PERIOD
        c16 += (Port << 2) * 0x100

        if(period == 0):
            period = int(1e9 / frequency)
        self.SafeSend161632(c16, c16, period | 0x80000000)
        self.WaitForACK()


    def DACStart(self, Port):
        """
        Starts the DAC port generator. The port must be initialised by the DACInit & DACGenerate methods

        Parameters:
            Port - DAC port number
        """

        self.counter += 1
        if(Port != self.DAC1 and Port != self.DAC2):
            return
        
        c16 = self.DAC_START
        c16 += (Port << 2) * 0x100
        
        self.Send16(c16)
        self.WaitForACK()
 

    def DACStop(self, Port, Voltage=0):
        """
        Stops the DAC port generator

        Parameters:
            Port - DAC port number
            Voltage - output voltage
        """

        self.counter += 1
        if(Port != self.DAC1 and Port != self.DAC2):
            return
        
        c16 = self.DAC_STOP
        c16 += (Port << 2) * 0x100
        
        self.Send16(c16)
        self.Send16(int(Voltage) | 0x8000)
 

    def PWMFrequencyDuty(self, Ports, frequency, period=-1, duty=0):
        """
        Sets the PWM port frequency and duty ratio. If the PWM channel is started it changes the frequency and the duty on the fly

        Parameters:
            Ports - list of the PWM ports to set the frequency / duty ratio
            frequency - frequency in Hz
            period - period in ns
            ratio - duty ratio in % (0 - 100%)
        """
        self.counter += 1
        if (frequency == -1 and period == -1):
            return
        if duty < 0:
            duty = 0
        if duty > 100:
            duty = 100

        dutyint = int(0x7fff * duty / 100)
        CodedPorts = self.CodePortNumbers(Ports)
        if(CodedPorts[1] == 0):
            return
        if period == -1:
            period = 1e9 / frequency
        c16 = self.PWM_FREQ_DUTY_L
        self.SafeSend16323216(c16, CodedPorts[0], int(period) | 0x80000000, dutyint | 0x8000)
        self.WaitForACK()

    def PWMFrequency(self, Ports, frequency, period=-1):
        """
        Sets the PWM ports frequency 

        Parameters:
            Ports - list of the PWM ports to set the frequency / duty ratio
            frequency - frequency in Hz
            period - period in ns
        """
        self.counter += 1
        if (frequency == -1 and period == -1):
            return
        CodedPorts = self.CodePortNumbers(Ports)
        if(CodedPorts[1] == 0):
            return
        if period == -1:
            period = 1e9 / frequency
        c16 = self.PWM_FREQ_L
        self.SafeSend163232(c16, CodedPorts[0], int(period) | 0x80000000)
        self.WaitForACK()
        
    def PWMDuty(self, Ports, duty=-1):
        """
        Sets the PWM ports duty ratio. If the PWM channel is started it changes the duty on the fly

        Parameters:
            Ports - list of the PWM ports to set the frequency / duty ratio
            ratio - duty ratio in % (0 - 100%)
        """
        self.counter += 1
        if duty < 0:
            duty = 0
        if duty > 100:
            duty = 100

        dutyint = int(0x7fff * duty / 100)
        CodedPorts = self.CodePortNumbers(Ports)
        if(CodedPorts[1] == 0):
            return
        c16 = self.PWM_DUTY_L
        self.SafeSend163216(c16, CodedPorts[0], dutyint | 0x8000)
        self.WaitForACK()

    def PWMInit(self, Ports, frequency=0, period=0, duty=0):
        """
        Initialises the PWM ports

        Parameters:
            Ports - list of the PWM ports to set the frequency / duty ratio
            frequency - frequency in Hz
            period - period in ns
            ratio - duty ratio in % (0 - 100%)
        """
        self.counter += 1
        c16 = self.PWM_INIT_L
        CodedPorts = self.CodePortNumbers(Ports)
        if(CodedPorts[1] == 0):
            return
        self.SafeSend1632(c16, CodedPorts[0])
        self.WaitForACK()
        if frequency != 0 or period != 0 or duty != 0:
            self.PWMFrequency(Ports, frequency = frequency, period = period, duty = duty)
            self.WaitForACK()

    def PWMStart(self, Ports):
        """
        Starts PWM generation on the selected ports

        Parameters:
            Ports - list of the PWM ports to set the frequency / duty ratio
        """
        self.counter += 1
        c16 = self.PWM_START_L
        CodedPorts = self.CodePortNumbers(Ports)
        if(CodedPorts[1] == 0):
            return
        self.SafeSend1632(c16, CodedPorts[0])
        self.WaitForACK()

    def SERVOInit(self, ports, frequency=50, minimum=1000000, maximum=2000000, centre=1500000, exponential=0):
        """
        Initialises the servo port (or PWM port to generate th RC PWM servo signal)

        Parameters:
            Ports - list of the ports
            frequency - frequency of the generated signal. Standard servos require 20ms time between the impluses. High speed servos may accept the higher rates
            minimum - minimum impulse width in ns. For standard servos it is 1ms = 1000000ns
            centre - centre position impulse width in ns. For standard servos it is 1.5ms = 1500000ns
            maximum - minimum impulse width in ns. For standard servos it is 2ms = 2000000ns
            expotential - expo ratio. For the explanation please visit: https://www.desmos.com/calculator/x3utvihals
        """
        self.counter += 1
        if minimum == 0 or maximum == 0 or centre == 0 or frequency == 0:
            return
        c16 = self.SERVO_INIT
        CodedPorts = self.CodePortNumbers(ports)
        if(CodedPorts[1] == 0):
            return
        Period = 1e9 / frequency
        for port in ports:
            self.servo[port] = [Period, minimum, maximum, centre, exponential]
        self.PWMInit(ports)
        self.PWMFrequencyDuty(ports, frequency = frequency, duty = 100.0 * centre / 20000000)
        self.PWMStart(ports)
        self.SafeSend16323232323216(c16, CodedPorts[0], self.CD32(Period), self.CD32(minimum), self.CD32(maximum), self.CD32(centre), self.CD16(exponential * 100))
        self.WaitForACK()

    def GetExpo(self, val, maximum, expo):
        result = val * math.exp(expo * abs(val) / maximum - expo)
        if result < -maximum:
            result = -maximum
        if result > maximum:
            result = maximum
        
        return result

    def SERVOSetPos(self, ports, position):   #-100 : 100 - exponent is taken from the first port in the list
        """
        Sets the servo position

        Parameters:
            Ports - list of the ports
            osition - servo position in %. 0% - centre point, -100% minimum position, 100% maximum position
        """
        self.counter += 1
        if position < -100:
            position = -100
        if position > 100:
            position = 100

        position = self.GetExpo(position, 100,  self.servo[ports[0]][4])
        position += 100

        CodedPorts = self.CodePortNumbers(ports)
        if(CodedPorts[1] == 0):
            return

        servoduty = int((position / 200.0) * 0x7fff)
        c16 = self.SERVO_SET
        
        self.SafeSend163216(c16, CodedPorts[0], self.CD16(servoduty))
        self.WaitForACK()

    def ADCInit(self, Ports,speed = 0xff):
        """
        Initialises the ADC ports

        Parameters:
            Ports - list of the ports
            speed - sample time:
            S = sample time:
                    0 23.4ns
                    1 39.1ns
                    2 70.3ns
                    3 117.2ns
                    4 304.7ns
                    5 960.9ns
                    6 2835.9ns
                    7 9398.4ns
                    0xff (dflt) 117.2ns
        """
        self.counter += 1
        if speed < 0 or speed > 7:
            sample = 0xff
        else:
           sample = speed
        c16 = self.ADC_INIT_L | (int(sample) << 8)
        CodedPorts = self.CodePortNumbers(Ports)
        if(CodedPorts[1] == 0):
            return
        self.SafeSend1632(c16, CodedPorts[0])
        self.WaitForACK()

    def ADCReadVref(self):
        """
        Reads the Voltage reference

        Parameters:
            none
        Return the reference voltage in mV
        """
        self.counter += 1
        c16 = self.ADC_READ_VREF
        self.SafeSend16(c16)
        self.Vref = (self.Read16() & 0x0fff) / 1000.0
        self.WaitForACK()
        return self.Vref

    def ADCRead(self, ports, speed = 0xff):
        """
        Reads the ADC ports

        Parameters:
            Ports - list of the ports
            speed - sample time:
            S = sample time:
                    0 23.4ns
                    1 39.1ns
                    2 70.3ns
                    3 117.2ns
                    4 304.7ns
                    5 960.9ns
                    6 2835.9ns
                    7 9398.4ns
                    0xff (dflt) 117.2ns
            returns list of lists. List 0 - raw values (0-4095), List 1 - voltage in mV
        """
        self.counter += 1
        divider = (1 << self.ADCResolution) - 1.0
        data = [[],[]]
        for port in range(0,30) :
            data[0].append(0)
            data[1].append(0)
        if speed < 0 or speed > 7:
            sample = 0xff
        else:
           sample = speed
        c16 = self.ADC_READ_L | (int(sample) << 8)
        CodedPorts = self.CodePortNumbers(ports)
        if(CodedPorts[1] == 0):
            return
        s = signal.signal(signal.SIGINT, signal.SIG_IGN)
        self.SafeSend1632(c16, CodedPorts[0])
        nchannels = self.Read16()
        if(nchannels != CodedPorts[1]):
            data[0][29] = -1;
        while nchannels != 0:
            readdata = self.Read16()
            port = (readdata & 0xf000) >> 12
            readdata = readdata & 0xfff
            data[0][self.ADC_CONVTABLE[port - 1]] = readdata
            data[1][self.ADC_CONVTABLE[port - 1]] = (readdata * self.Vref) / divider
            nchannels -= 1
        signal.signal(signal.SIGINT, s) 
        self.WaitForACK()
        return data

    def ADCReadData(self, ports, speed = 0xff, nsamples = 0, frequency = 0, period = 0):
        """
        Reads set of data results from ADC ports

        Parameters:
            Ports - list of the ports
            speed - sample time:
            S = sample time:
                    0 23.4ns
                    1 39.1ns
                    2 70.3ns
                    3 117.2ns
                    4 304.7ns
                    5 960.9ns
                    6 2835.9ns
                    7 9398.4ns
                    0xff (dflt) 117.2ns
            nsmaples - number of samples to be read in one period (1/frequency). The actual time between reads is period / nsamples
            frequency - frequency in Hz
            period - period in ns
            returns list of lists of the list. List 0 - list of lists of results, list[port][0] - raw values (0-4095), list[port][0] - voltage in mV
        """
        self.counter += 1
        divider = (1 << self.ADCResolution) - 1.0
        data = []
        for port in range(0,30) :
            data.append([[],[]])
        if speed < 0 or speed > 7:
            sample = 0xff
        else:
            sample = int(speed) & 7
        c16 = self.ADC_READ_FAST | (int(sample) << 8)
        CodedPorts = self.CodePortNumbers(ports)
        if(CodedPorts[1] == 0):
            return
        if nsamples <= 0 or (frequency <= 0 and period <= 0):
            return
        if frequency != 0:
            period = int(1e9 / frequency)
        s = signal.signal(signal.SIGINT, signal.SIG_IGN)
        self.SafeSend16323216(c16, CodedPorts[0], period, nsamples)
        nchannels = self.Read16()
        while nchannels != 0:
            readdata = self.Read16()
            port = (readdata & 0xf000) >> 12
            readdata = readdata & 0xfff
            data[self.ADC_CONVTABLE[port - 1]][0].append(readdata)
            data[self.ADC_CONVTABLE[port - 1]][1].append((readdata * self.Vref) / divider)
            nchannels -= 1
        signal.signal(signal.SIGINT, s) 
        self.WaitForACK()
        return data


    def IMPULSERead(self, Port, mode = 0, edge = 1):
        """
        Gets impulse width, frequency of the signal, or frequency and duty ratio of the signal

        Parameters:
            Port -  GPIO port number
            mode -  0 - impullse width
                    1 - frequency and duty ratio of the PWM signal
                    2 - frequency
            edge -  initial edge of the signal (1 rising, 0 falling)
        
        Return values:
            [result1, result2]
                result1 -   in mode 0 - width of the impulse in the 1/64000000 s units
                        -   in mode 1 - impulse width of the first part of the PWM signal in the 1/64000000 s units
                        -   in mode 2 - period of the signal in the 1/64000000 s units
                result2 -   in mode 1 - impulse width of the second part of the PWM signal in the 1/64000000 s units
        """
        self.counter += 1
        result = []
        if edge != 0:
            edge = 1
        if mode < 0 or mode > 2:
            mode = 0
        c16 = int(Port) << 11
        c16 |= int(mode) << 9
        c16 |= int(edge) << 8
        c16 |= self.IMPULSE_READ
        self.SafeSend16(c16)
        counter = self.Read32()
        counter = self.decode32(counter)
        counter -= 1
        for i in range(0, 3):
            tmpres = [self.Read32(), self.Read32()]
            tmpres[0] = self.decode32(tmpres[0])
            tmpres[1] = self.decode32(tmpres[1])
            result.append(tmpres)
        self.WaitForACK()
        result1 = counter * result[1][1] + (counter - result[1][0]) - (counter * result[0][1] + (counter - result[0][0]))
        result2 = counter * result[2][1] + (counter - result[2][0]) - (counter * result[1][1] + (counter - result[1][0]))
        AllZeroes = True
        for res in result:
            for value in res:
                if value != 0:
                    AllZeroes = False;
        if AllZeroes: 
            return[-1,-1]
        if result1 < 0 or (result2 < 0 and mode == 1):
            return[0, -1]
        if result[0][1] == 0x3ffffffff and result [0][0] == 0x3ffffffff:
            return[-1, 0]
        return [result1, result2]
