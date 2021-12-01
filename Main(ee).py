from ComponentModule.InputComponentPackage.UltrasonicSensor import *
from ComponentModule.InputComponentPackage.LightSensor import *
from time import *
from Firebase import Firebase
import threading

e = threading.Event()
db = Firebase()

def main():    
    # region : sensor declaration section
    ultrasonic_sensor = UltrasonicSensor(1)
    light_sensor = LightSensor(14)
    # endregion    
    
    
    lights = db.read("traffic_lights/order")
        
    traffic_lights_stream = db.read_live("traffic_lights/order",stream_handler)
    traffic_lights_ambulance_stream = db.read_live("traffic_lights/have_ambulance",stream_detect_ambulance)
    
    while True:
        try:            
            print("hello")
            e.wait(5)
            lights = lights[1:] + [lights[0]]            
            db.update("traffic_lights",{"order":lights})            
        except KeyboardInterrupt:
            #my_stream.close()
            break
        except TypeError:
            print("Type Error occurs")
            #my_stream.close()
            break
        except IOError:
            print("IO Error Occurs")
            #my_stream.close()
            break
            
    traffic_lights_stream.close()
    traffic_lights_ambulance_stream.close()


def stream_handler(message):    
    data = message["data"]
    print(data)
    if(data[0]=="light1"):
        print("light1 go!")
    if(data[0]=="light2"):
        print("light2 go!")
    if(data[0]=="light3"):
        print("light3 go!")

# for receiving part, not sending part
def stream_detect_ambulance(message):
    have_ambulance_traffic_light = message["data"]
    print(have_ambulance_traffic_light)
    if(have_ambulance_traffic_light != ""):        
        if(have_ambulance_traffic_light != "traffic_light1"): #equal to self
            order_data = db.read("traffic_lights/order")
            print(f"order_data = ${order_data}")
            if(order_data[0] == "traffic_light1"):
                print("interrupted")
                e.set()
                #store remaining_seconds
                #stop calling the code inside *while loop* (maybe put it inside a method?)
    else:
        pass
        #start calling the code inside *while loop* (maybe put it inside a method?)
    

main()

