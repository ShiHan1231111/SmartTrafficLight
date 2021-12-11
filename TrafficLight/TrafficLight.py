import asyncio

from ComponentModule.OutputComponentPackage.GroveRelay import *
from ComponentModule.InputComponentPackage.LightCheckPin import *
import time
from grovepi import *
from pyrebase import pyrebase
from Firebase import Firebase
fb = Firebase()


class TrafficLight(object):
    def __init__(self, traffic_id, red_pin, yellow_pin, green_pin, red_check_pin, yellow_check_pin, green_check_pin):
        self.name = traffic_id
        self.redLight = GroveRelay(red_pin)
        self.yellowLight = GroveRelay(yellow_pin)
        self.greenLight = GroveRelay(green_pin)
        self.greenLight.turn_on()
        self.checkRed = LightCheckPin(red_check_pin)
        self.checkYellow = LightCheckPin(yellow_check_pin)
        self.checkGreen = LightCheckPin(green_check_pin)


    '''
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

async def check_yellow_light(self):
        for loop_count in range(5):
            await asyncio.sleep(0.00001)
            yellow_condition = self.checkYELLOW.get_status()
            if yellow_condition == 1:
                print("Yellow LED light has malfunctioned")
            else:
                print("Yellow LED light is functioning")

            await asyncio.sleep(1)


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
'''

    def report_faulty_red(self):
        fb.update(f"TrafficLights/{self.name}/Red_Light", {"status": "faulty", "malf_timestamp": fb.create_time_stamp()})
        fb.append("/Notifications/notification", {"unread": True, "title": f"{self.name} Red Light has malfunctioned", "timestamp": fb.create_time_stamp()})

    def report_faulty_yellow(self):
        fb.update(f"TrafficLights/{self.name}/Yellow_Light", {"status": "faulty", "malf_timestamp": fb.create_time_stamp()})
        fb.append("/Notifications/notification", {"unread": True, "title": f"{self.name} Yellow Light has malfunctioned", "timestamp": fb.create_time_stamp()})

    def report_faulty_green(self):
        fb.update(f"TrafficLights/{self.name}/Green_Light", {"status": "faulty", "malf_timestamp": fb.create_time_stamp()})
        fb.append("/Notifications/notification", {"unread": True, "title": f"{self.name} Green Light has malfunctioned", "timestamp": fb.create_time_stamp()})

    def traffic_light_down(self):
        fb.append(f"TrafficLights/{self.name}", {"status": 0})
        fb.append(f"TrafficLights/{self.name}/malf_timestamp", {"timestamp": fb.convert_timestamp(time.time())})

    def red_light_ok(self):
        fb.update(f"TrafficLights/{self.name}/Red_Light", {"status":1, "malf_timestamp":0})
        fb.append("/Notifications/notification", {"unread": True, "title": f"Malfunctioned {self.name} Green Light has been fixed", "timestamp": fb.create_time_stamp()})

    def yellow_light_ok(self):
        fb.update(f"TrafficLights/{self.name}/Yellow_Light", {"status":1, "malf_timestamp":0})
        fb.append("/Notifications/notification", {"unread": True, "title": f"Malfunctioned {self.name} Green Light has been fixed", "timestamp": fb.create_time_stamp()})

    def green_light_ok(self):
        fb.update(f"TrafficLights/{self.name}/Green_Light", {"status":1, "malf_timestamp":0})
        fb.append("/Notifications/notification", {"unread": True, "title": f"Malfunctioned {self.name} Green Light has been fixed", "timestamp": fb.create_time_stamp()})

    def traffic_light_fixed(self):
        fb.append(f"TrafficLights/{self.name}", {"status": 1})
        fb.append(f"TrafficLights/{self.name}/malf_timestamp", {"timestamp": fb.convert_timestamp(time.time())})









