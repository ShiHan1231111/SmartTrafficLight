from ComponentModule.InputComponentPackage.InputComponent import InputComponent
from FakeDevices import *


class LightSensor(InputComponent):
    def __init__(self, pin_number):
        super().__init__(pin_number)

    def get_light_intensity(self):
        return str(analogRead(self.pin_number))
