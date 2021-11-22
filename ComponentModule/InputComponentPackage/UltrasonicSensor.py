from ComponentModule.InputComponentPackage.InputComponent import InputComponent
from FakeDevices import *


class UltrasonicSensor(InputComponent):
    def __init__(self, pin_number):
        super().__init__(pin_number)

    def get_distance(self):
        return str(ultrasonicRead(self.pin_number))
