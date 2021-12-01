from ComponentModule.InputComponentPackage.InputComponent import InputComponent
from grovepi import *


class LightCheckPin(InputComponent):
    def __init__(self, pin_number):
        super().__init__(pin_number)

    def get_status(self):
        return digitalRead(self.pin_number)