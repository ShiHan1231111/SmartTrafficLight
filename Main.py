from ComponentModule.OutputComponentPackage.GroveRelay import *
from ComponentModule.InputComponentPackage.LightCheckPin import *
from TrafficLight import *
from time import *
from grovepi import *
from pyrebase import pyrebase
from Firebase import Firebase
db = Firebase()

# region : traffic light declaration section
redLED = 2
yellowLED = 3
greenLED = 4
checkRED = 5
checkYELLOW = 6
checkGREEN = 7
traffic_id="traffic_light1"

# endregion

tf1 = TrafficLight(traffic_id, redLED, yellowLED, greenLED, checkRED, checkYELLOW, checkGREEN)


def main():
    red_light_good = True
    green_light_good = True
    yellow_light_good = True
    while True:
        try:
            light_time = 5
            sleep(5)
            '''
            red_light_process = multiprocessing.Process(target=check_red_light, args=(light_time, ))
            red_light_process.start()
            red_light(light_time)

            green_light_process = multiprocessing.Process(target=check_green_light, args=(light_time, ))
            green_light_process.start()
            green_light(light_time)


            yellow_light_process = multiprocessing.Process(target=check_yellow_light, args=())
            yellow_light_process.start()
            yellow_light()
            '''
            if red_light_good is not True or green_light_good is not True or yellow_light_good is not True:
                tf1.fault_shutdown()
            else:
                red_light_good = tf1.red_light(light_time)

            if red_light_good is not True or green_light_good is not True or yellow_light_good is not True:
                tf1.fault_shutdown()
            else:
                green_light_good = tf1.green_light(light_time)

            if red_light_good is not True or green_light_good is not True or yellow_light_good is not True:
                tf1.fault_shutdown()
            else:
                yellow_light_good = tf1.yellow_light()

            [red_light_good, green_light_good, yellow_light_good] = tf1.check_lights_again()
            if red_light_good is True and green_light_good is True and yellow_light_good is True:
                db.update(f"traffic_lights/{traffic_id}", {"status": 1})
                db.append(f"traffic_lights/{traffic_id}/malf_timestamp",
                          {"timestamp": db.convert_timestamp(time.time())})

        except KeyboardInterrupt:
            break
        except TypeError:
            print("Type Error occurs")
            break
        except IOError:
            print("IO Error Occurs")
            break


main()
