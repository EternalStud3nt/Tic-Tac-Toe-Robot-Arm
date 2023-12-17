#!/usr/bin/python

import time
from PCA9685 import PCA9685  # Make sure PCA9685.py is in the same directory

if __name__ == '__main__':
    pwm = PCA9685(0x40, debug=False)
    pwm.setPWMFreq(50)
    try:
        while True:
            on_input = input("Enter 'on' value (0-4095): ")
            off_input = input("Enter 'off' value (0-4095): ")

            on_value = int(on_input)
            off_value = int(off_input)

            if 0 <= on_value <= 4095 and 0 <= off_value <= 4095:
                pwm.setPWM(0, on_value, off_value)
                print(f"Set PWM values: 'on' = {on_value}, 'off' = {off_value}")
            else:
                print("Invalid input. Values should be between 0 and 4095.")
    except KeyboardInterrupt:
        print("\nExiting the program.")
