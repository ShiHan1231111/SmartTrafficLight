from ComponentModule.InputComponentPackage.UltrasonicSensor import *
from time import *


def main():
    # region : sensor declaration section
    ultrasonic_sensor = UltrasonicSensor(1)
    # endregion

    while True:
        try:
            print(ultrasonic_sensor.get_distance())
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
