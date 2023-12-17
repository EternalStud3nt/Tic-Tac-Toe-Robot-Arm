#!/usr/bin/python

import time
from PCA9685 import PCA9685  # Make sure PCA9685.py is in the same directory

if __name__ == '__main__':
    pwm = PCA9685(0x40, debug=False)
    pwm.setPWMFreq(50)
    try:
        while True:
            channel_input = input("Enter channel number (0-15): ")
            on_input = input("Enter 'on' value (0-4095): ")
            off_input = input("Enter 'off' value (0-4095): ")

            channel = int(channel_input)
            on_value = int(on_input)
            off_value = int(off_input)

            if 0 <= channel <= 15 and 0 <= on_value <= 4095 and 0 <= off_value <= 4095:
                pwm.setPWM(channel, on_value, off_value)
                print(f"Set PWM values for channel {channel}: 'on' = {on_value}, 'off' = {off_value}
