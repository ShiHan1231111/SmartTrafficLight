from ComponentModule.InputComponentPackage.UltrasonicSensor import *
from ComponentModule.InputComponentPackage.LightSensor import *
from time import *


def main():
    # region : sensor declaration section
    ultrasonic_sensor = UltrasonicSensor(1)
    light_sensor = LightSensor(14)
    # endregion

    while True:
        try:
            print(ultrasonic_sensor.get_distance())
            print(light_sensor.get_light_intensity())
            sleep(1)

        except KeyboardInterrupt:
            break

        except TypeError:
            print("Type Error occurs")
            break
        except IOError:
            print("IO Error Occurs")
            break


main()
