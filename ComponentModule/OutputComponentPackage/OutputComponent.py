from ComponentModule.Component import Component
from FakeDevices import *


class OutputComponent(Component):
    def __init__(self, pin_number):
        self.PIN_MODE = "OUTPUT"
        super().__init__(pin_number)
        pinMode(pin_number, self.PIN_MODE)
