import logging
from FakeDevices import *

try:
    gui = Gui()

    gui.add(DigitalPin(4, 'RED LED LIGHT'))
    gui.add(DigitalPin(3, 'YELLOW LED LIGHT'))
    gui.add(DigitalPin(2, 'GREEN LED LIGHT'))

    gui.add(DigitalPin(7, 'CHECK RED LIGHT'))
    gui.add(DigitalPin(8, 'CHECK YELLOW LIGHT'))
    gui.add(DigitalPin(5, 'CHECK GREEN LIGHT'))

    from ComponentSimulation.TL002 import *
except:
    logging.exception('-------------Log-------------------')

gui.quit()

print("Program Terminated")
