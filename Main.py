from ComponentModule.InputComponentPackage.UltrasonicSensor import *
from ComponentModule.InputComponentPackage.LightSensor import *
from ComponentModule.OutputComponentPackage.GroveRelay import *
from ComponentModule.InputComponentPackage.LightCheckPin import *

from time import *
from grovepi import *
from pyrebase import pyrebase


config = {
    "apiKey":"AIzaSyDGGWQfuvSiiCPpL2MUIJi1HO_TdmscVlY",
    "authDomain":"bait2123-iot-b0887.firebaseapp.com",
    "databaseURL":"https://bait2123-iot-b0887-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "storageBucket":"gs://bait2123-iot-b0887.appspot.com",
}

try:
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    user = auth.sign_in_with_email_and_password("kchongee@gmail.com","zt/h!\!*B;{)8/U$")
    db = firebase.database()
    storage = firebase.storage()
except Exception as e:
    print(e)
    exit(-1)


# region : sensor declaration section
redLED = GroveRelay(2)
yellowLED = GroveRelay(3)
greenLED = GroveRelay(4)

checkRED = LightCheckPin(5)
checkYELLOW = LightCheckPin(6)
checkGREEN = LightCheckPin(7)
# endregion


def red_light(red_time):
    redLED.turn_on()
    is_red_functioning=check_red_light(red_time)
    redLED.turn_off()
    if is_red_functioning:
        return True
    else:
        return False


def yellow_light():
    yellowLED.turn_on()
    is_yellow_functioning=check_yellow_light()
    yellowLED.turn_off()
    if is_yellow_functioning:
        return True
    else:
        return False


def green_light(green_time):
    greenLED.turn_on()
    is_green_functioning=check_green_light(green_time)
    greenLED.turn_off()
    if is_green_functioning:
        return True
    else:
        return False


def check_red_light(red_time):
    for loop_count in range(math.floor(red_time)):
        red_condition=checkRED.get_status()
        if red_condition==1:
            print("Red LED light has malfunctioned")
            return False
        else:
            print("Red LED light is functioning")
        sleep(1)
    return True


def check_yellow_light():
    for loop_count in range(5):
        yellow_condition=checkYELLOW.get_status()
        if yellow_condition==1:
            print("Yellow LED light has malfunctioned")
            return False
        else:
            print("Yellow LED light is functioning")
        sleep(1)
    return True


def check_green_light(green_time):
    for loop_count in range(math.floor(green_time)):
        green_condition=checkGREEN.get_status()
        if green_condition==1:
            print("Green LED light has malfunctioned")
            return False
        else:
            print("Green LED light is functioning")
        sleep(1)
    return True


def fault_shutdown():
    redLED.turn_off()
    yellowLED.turn_off()
    greenLED.turn_off()
    return


def check_lights_again():
    check_values = [not (bool(checkRED.get_status())),
                    not (bool(checkGREEN.get_status())),
                    not (bool(checkYELLOW.get_status()))]
    return check_values


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
                fault_shutdown()
            else:
                red_light_good = red_light(light_time)

            if red_light_good is not True or green_light_good is not True or yellow_light_good is not True:
                fault_shutdown()
            else:
                green_light(light_time)

            if red_light_good is not True or green_light_good is not True or yellow_light_good is not True:
                fault_shutdown()
            else:
                yellow_light()

            [red_light_good, green_light_good, yellow_light_good] = check_lights_again()

        except KeyboardInterrupt:
            break
        except TypeError:
            print("Type Error occurs")
            break
        except IOError:
            print("IO Error Occurs")
            break


main()
