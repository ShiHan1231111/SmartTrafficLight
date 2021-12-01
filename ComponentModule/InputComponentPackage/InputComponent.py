from ComponentModule.Component import Component
from grovepi import *


class InputComponent(Component):
    def __init__(self, pin_number):
        self.PIN_MODE = "INPUT"
        self.pin_number = pin_number
        super().__init__(pin_number)
        pinMode(pin_number, self.PIN_MODE)
