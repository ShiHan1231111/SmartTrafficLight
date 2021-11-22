import logging

from ComponentModule.InputComponentPackage.UltrasonicSensor import UltrasonicSensor
from FakeDevices import *

try:
    gui = Gui()
    gui.add(Ultrasonic(1, 'ultrasonicDevice'))
    from Main import *
except:
    logging.exception('-------------Log-------------------')
