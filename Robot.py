#!/usr/bin/python

import time
from PCA9685 import PCA9685  # Make sure PCA9685.py is in the same directory

if __name__ == '__main__':
    pwm = PCA9685(0x40, debug=False)
    pwm.setPWMFreq(50)
    try:
        while True:
            channel_input = input("Enter channel number (0-15): ")
            pulse_input = input("Enter pulse width (500 - 2500): ")

            channel = int(channel_input)
            pulse = int(pulse_input)

            if 0 <= channel <= 15:
                pwm.setServoPulse(channel, pulse)
                print(f"Set pulse {pulse}us for channel {channel}.")
            else:
                print("Invalid input. Channel should be between 0 and 15")
    except KeyboardInterrupt:
        print("\nExiting the program.")
