#!/usr/bin/python

import time
from PCA9685 import PCA9685  # Assuming PCA9685 class is in PCA9685.py file

if __name__=='__main__':
    
    # Create PCA9685 object
    pwm = PCA9685(0x40, debug=False)
    
    # Set PWM frequency to 50 Hz
    pwm.setPWMFreq(50)
    
    try:
        while True:
            # Ask the user for input
            pulse_input = input("Enter pulse duration (500-2500): ")
            
            # Convert user input to an integer
            pulse_value = int(pulse_input)
            
            # Validate the input range
            if 500 <= pulse_value <= 2500:
                # Set the servo pulse based on user input
                pwm.setServoPulse(0, pulse_value)
                print(f"Set servo pulse to {pulse_value}")
            else:
                print("Invalid input. Pulse duration should be between 500 and 2500.")
    
    except KeyboardInterrupt:
        print("\nExiting the program.")
