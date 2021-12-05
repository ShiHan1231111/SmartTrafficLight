from ComponentModule.InputComponentPackage.UltrasonicSensor import *
from ComponentModule.InputComponentPackage.LightSensor import *
import time
from Firebase import Firebase
import threading
import random

e = threading.Event()
db = Firebase()

def main():    
    # region : sensor declaration section
    ultrasonic_sensor = UltrasonicSensor(1)
    light_sensor = LightSensor(14)
    # endregion    
    
    push_dummy_data()
    print("finish")
    return ""    
    
    '''
    db.refresh_data()
    
    lights = db.read("traffic_lights/order")
        
    traffic_lights_stream = db.read_live("traffic_lights/order",stream_handler)
    traffic_lights_ambulance_stream = db.read_live("traffic_lights/have_ambulance",stream_detect_ambulance)
    '''
    
    while True:
        try:
            '''
            print("hello")
            e.wait(5)
            lights = lights[1:] + [lights[0]]            
            db.update("traffic_lights",{"order":lights})
            '''
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

def convertTimestamp(timestamp):
    return round((timestamp)*1000)

def push_dummy_data():
    for i in range(10):
        db.append("/roads/road1",{"carCount":random.randint(0,101),"timestamp":convertTimestamp(time.time())})
        '''
        db.append("/roads/road2",{"carCount":random.randint(0,101),"timestamp":convertTimestamp(time.time())})
        db.append("/roads/road3",{"carCount":random.randint(0,101),"timestamp":convertTimestamp(time.time())})
        db.append("/ambulance/traffic_light1",{"timestamp":convertTimestamp(time.time())})
        db.append("/ambulance/traffic_light2",{"timestamp":convertTimestamp(time.time())})
        db.append("/ambulance/traffic_light3",{"timestamp":convertTimestamp(time.time())})
        db.append("/notifications/notification",{"title":"It was always the Monday mornings. It never seemed to happen on Tuesday morning, Wednesday morning, or any other morning during the week. But it happened every Monday morning like clockwork. He mentally prepared himself to once again deal with what was about to happen, but this time he also placed a knife in his pocket just in case.","timestamp":convertTimestamp(time.time())})
        db.append("/notifications/notification",{"title":"The rain and wind abruptly stopped, but the sky still had the gray swirls of storms in the distance. Dave knew this feeling all too well. The calm before the storm. He only had a limited amount of time before all Hell broke loose, but he stopped to admire the calmness. Maybe it would be different this time, he thought, with the knowledge deep within that it wouldn't.","timestamp":convertTimestamp(time.time())})
        db.append("/notifications/notification",{"title":"She patiently waited for his number to be called. She had no desire to be there, but her mom had insisted that she go. She's resisted at first, but over time she realized it was simply easier to appease her and go. Mom tended to be that way. She would keep insisting until you wore down and did what she wanted. So, here she sat, patiently waiting for her number to be called.","timestamp":convertTimestamp(time.time())})
        db.append("/notifications/notification",{"title":"Patricia's friend who was here hardly had any issues at all, but she wasn't telling the truth. Yesterday, before she left to go home, she heard that her husband is in the hospital and pretended to be surprised. It later came out that she was the person who had put him there.","timestamp":convertTimestamp(time.time())})
        db.append("/turning",{"left":random.randint(0,101),"right":random.randint(0,101),"timestamp":convertTimestamp(time.time())})
        '''

main()

