from ComponentModule.OutputComponentPackage.OutputComponent import OutputComponent
from grovepi import *


class GroveRelay(OutputComponent):
    def __init__(self, pin_number):
        print(f"pin number is {pin_number}")
        super().__init__(pin_number)

    def turn_on(self):
        digitalWrite(self.pin_number, 1)

    def turn_off(self):
        digitalWrite(self.pin_number, 0)

