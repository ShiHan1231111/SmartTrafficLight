import logging

from ComponentModule.InputComponentPackage.UltrasonicSensor import UltrasonicSensor
from FakeDevices import *

try:
    gui = Gui()
    gui.add(Ultrasonic(1, 'ultrasonicDevice'))
    gui.add(AnalogReadPin(14, 'Light Sensor'))
    from Main import *
except:
    logging.exception('-------------Log-------------------')
