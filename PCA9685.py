#!/usr/bin/python

import time
import math
import smbus

# ============================================================================
# Raspi PCA9685 16-Channel PWM Servo Driver
# ============================================================================

class PCA9685:

    # I2C register addresses
    __SUBADR1            = 0x02
    __SUBADR2            = 0x03
    __SUBADR3            = 0x04
    __MODE1              = 0x00
    __PRESCALE           = 0xFE
    __LED0_ON_L          = 0x06
    __LED0_ON_H          = 0x07
    __LED0_OFF_L         = 0x08
    __LED0_OFF_H         = 0x09
    __ALLLED_ON_L        = 0xFA
    __ALLLED_ON_H        = 0xFB
    __ALLLED_OFF_L       = 0xFC
    __ALLLED_OFF_H       = 0xFD

    def __init__(self, address=0x40, debug=False):
        # Initialize PCA9685 object
        self.bus = smbus.SMBus(1)
        self.address = address
        self.debug = debug
        
        # Reset PCA9685 to initialize
        if (self.debug):
            print("Reseting PCA9685")
        self.write(self.__MODE1, 0x00)
    
    def write(self, reg, value):
        # Writes an 8-bit value to the specified register/address
        self.bus.write_byte_data(self.address, reg, value)
        if (self.debug):
            print("I2C: Write 0x%02X to register 0x%02X" % (value, reg))
    
    def read(self, reg):
        # Read an unsigned byte from the I2C device
        result = self.bus.read_byte_data(self.address, reg)
        if (self.debug):
            print("I2C: Device 0x%02X returned 0x%02X from reg 0x%02X" % (self.address, result & 0xFF, reg))
        return result
    
    def setPWMFreq(self, freq):
        # Sets the PWM frequency
        # Calculate prescale value based on desired frequency
        prescaleval = 25000000.0    # 25MHz
        prescaleval /= 4096.0       # 12-bit
        prescaleval /= float(freq)
        prescaleval -= 1.0
        if (self.debug):
            print("Setting PWM frequency to %d Hz" % freq)
            print("Estimated pre-scale: %d" % prescaleval)
        
        # Set prescale for the PCA9685
        prescale = math.floor(prescaleval + 0.5)
        if (self.debug):
            print("Final pre-scale: %d" % prescale)
    
        # Save old mode, sleep, set prescale, restore old mode
        oldmode = self.read(self.__MODE1)
        newmode = (oldmode & 0x7F) | 0x10        # sleep
        self.write(self.__MODE1, newmode)        # go to sleep
        self.write(self.__PRESCALE, int(math.floor(prescale)))
        self.write(self.__MODE1, oldmode)
        time.sleep(0.005)
        self.write(self.__MODE1, oldmode | 0x80)

    def setPWM(self, channel, on, off):
        # Sets a single PWM channel
        # Directly controls the speed of the servo motor
        # Set PWM values for the specified channel
        self.write(self.__LED0_ON_L + 4 * channel, on & 0xFF)
        self.write(self.__LED0_ON_H + 4 * channel, on >> 8)
        self.write(self.__LED0_OFF_L + 4 * channel, off & 0xFF)
        self.write(self.__LED0_OFF_H + 4 * channel, off >> 8)
        if (self.debug):
            print("channel: %d  LED_ON: %d LED_OFF: %d" % (channel, on, off))
    
    def setServoPulse(self, channel, pulse):
        # Sets the Servo Pulse, assuming a PWM frequency of 50Hz
        # Determines the specific position or angle to which the servo motor should move
        # Convert pulse duration to PWM value
        pulse = pulse * 4096 / 20000        # PWM frequency is 50Hz, the period is 20000us
        self.setPWM(channel, 0, int(pulse))

if __name__=='__main__':
    
    # Create PCA9685 object
    pwm = PCA9685(0x40, debug=False)
    
    # Set PWM frequency to 50 Hz
    # Primarily influences how often the servo controller updates the position
    pwm.setPWMFreq(50)
    
    # Continuously sweep the servo back and forth
    while True:
        for i in range(500, 2500, 10):  
            pwm.setServoPulse(0, i)   
            time.sleep(0.02)     
        
        for i in range(2500, 500, -10):
            pwm.setServoPulse(0, i) 
            time.sleep(0.02)
         
         
# PULSE TO DEGREES IN "setServoPulse()"
# 500  -------   0 °
# 1000 -------  45 °
# 1500 -------  90 °
# 2000 ------- 135 °
# 2500 ------- 180 °            
