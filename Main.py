from ComponentModule.InputComponentPackage.UltrasonicSensor import *
from ComponentModule.InputComponentPackage.LightSensor import *
from time import *
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
    

def main():
    # region : sensor declaration section
    ultrasonic_sensor = UltrasonicSensor(1)
    light_sensor = LightSensor(14)
    # endregion

    while True:
        try:
            print(light_sensor.get_light_intensity())
            print(ultrasonic_sensor.get_distance())
            light_sensor.update(db)
            ultrasonic_sensor.update(db)
            sleep(2)

        except KeyboardInterrupt:
            break
        except TypeError:
            print("Type Error occurs")
            break
        except IOError:
            print("IO Error Occurs")
            break


main()