from ComponentModule.OutputComponentPackage.GroveRelay import *
from ComponentModule.InputComponentPackage.LightCheckPin import *

import time
from time import *
from grovepi import *
from pyrebase import pyrebase
from Firebase import Firebase
db = Firebase()


class TrafficLight:
    def __init__(self, traffic_id, red_pin, yellow_pin, green_pin, red_check_pin, yellow_check_pin, green_check_pin):
        self.name = traffic_id
        self.redLight = GroveRelay(red_pin)
        self.yellowLight = GroveRelay(yellow_pin)
        self.greenLight = GroveRelay(green_pin)

        self.checkRED = LightCheckPin(red_check_pin)
        self.checkYELLOW = LightCheckPin(yellow_check_pin)
        self.checkGREEN = LightCheckPin(green_check_pin)

    def red_light(self, red_time):
        self.redLight.turn_on()
        is_red_functioning = self.check_red_light(red_time)
        self.redLight.turn_off()
        if is_red_functioning:
            return True
        else:
            return False

    def yellow_light(self):
        self.yellowLight.turn_on()
        is_yellow_functioning = self.check_yellow_light()
        self.yellowLight.turn_off()
        if is_yellow_functioning:
            return True
        else:
            return False

    def green_light(self, green_time):
        self.greenLight.turn_on()
        is_green_functioning = self.check_green_light(green_time)
        self.greenLight.turn_off()
        if is_green_functioning:
            return True
        else:
            return False

    def check_red_light(self, red_time):
        for loop_count in range(math.floor(red_time)):
            sleep(0.00001)
            red_condition = self.checkRED.get_status()
            if red_condition == 1:
                print("Red LED light has malfunctioned")
                db.update(f"traffic_lights/{self.name}", {"status": 0})
                db.update(f"traffic_lights/{self.name}", {"malf_timestamp": db.convert_timestamp(time.time())})
                return False
            else:
                print("Red LED light is functioning")
                db.update(f"traffic_lights/{self.name}", {"status": 1})
            sleep(1)
        return True

    def check_yellow_light(self):
        for loop_count in range(5):
            sleep(0.00001)
            yellow_condition = self.checkYELLOW.get_status()
            if yellow_condition == 1:
                print("Yellow LED light has malfunctioned")
                return False
            else:
                print("Yellow LED light is functioning")
            sleep(1)
        return True

    def check_green_light(self, green_time):
        for loop_count in range(math.floor(green_time)):
            sleep(0.00001)
            green_condition = self.checkGREEN.get_status()
            if green_condition == 1:
                print("Green LED light has malfunctioned")
                return False
            else:
                print("Green LED light is functioning")
            sleep(1)
        return True

    def fault_shutdown(self):
        self.redLight.turn_off()
        self.yellowLight.turn_off()
        self.greenLight.turn_off()
        db.update(f"traffic_lights/{self.name}", {"status": 0})
        db.append(f"traffic_lights/{self.name}/malf_timestamp", {"timestamp": db.convert_timestamp(time.time())})
        return

    def check_lights_again(self):
        check_values = [not (bool(self.checkRED.get_status())),
                        not (bool(self.checkGREEN.get_status())),
                        not (bool(self.checkYELLOW.get_status()))]
        return check_values






