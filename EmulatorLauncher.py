import logging

from ComponentModule.InputComponentPackage.UltrasonicSensor import UltrasonicSensor
from FakeDevices import *

try:
    gui = Gui()
    gui.add(Ultrasonic(1, 'ultrasonicDevice'))
    gui.add(AnalogReadPin(14, 'Light Sensor'))

    gui.add(DigitalPin(2, 'RED LED LIGHT'))
    gui.add(DigitalPin(3, 'YELLOW LED LIGHT'))
    gui.add(DigitalPin(4, 'GREEN LED LIGHT'))

    gui.add(DigitalPin(5, 'CHECK RED LIGHT'))
    gui.add(DigitalPin(6, 'CHECK YELLOW LIGHT'))
    gui.add(DigitalPin(7, 'CHECK GREEN LIGHT'))

    from Main import *
except:
    logging.exception('-------------Log-------------------')

gui.quit()

print("Program Terminated")