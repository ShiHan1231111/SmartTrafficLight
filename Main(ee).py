from ComponentModule.InputComponentPackage.UltrasonicSensor import *
from ComponentModule.InputComponentPackage.LightSensor import *
import time
from Firebase import Firebase
import threading
import random
from twilio.rest import Client

e = threading.Event()
db = Firebase()
account_sid = "AC2df53bf36a712d732e12b1db71cf25e1"
auth_token = "c66631d83eaca5c894fcc427dc65c3c8"

def main():    
    # region : sensor declaration section
    ultrasonic_sensor = UltrasonicSensor(1)
    light_sensor = LightSensor(14)
    # endregion
        
    push_malfunc_notification("TL001","Red_Light",curr_status=0)
    
    '''
    push_dummy_data()
    print("finish")
    return ""
    '''
    
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
        '''
        db.append("/ambulance/traffic_light1",{"timestamp":convertTimestamp(time.time())})
        db.append("/ambulance/traffic_light2",{"timestamp":convertTimestamp(time.time())})
        db.append("/ambulance/traffic_light3",{"timestamp":convertTimestamp(time.time())})
        db.append("/notifications/notification",{"title":"It was always the Monday mornings. It never seemed to happen on Tuesday morning, Wednesday morning, or any other morning during the week. But it happened every Monday morning like clockwork. He mentally prepared himself to once again deal with what was about to happen, but this time he also placed a knife in his pocket just in case.","timestamp":convertTimestamp(time.time())})
        db.append("/notifications/notification",{"title":"The rain and wind abruptly stopped, but the sky still had the gray swirls of storms in the distance. Dave knew this feeling all too well. The calm before the storm. He only had a limited amount of time before all Hell broke loose, but he stopped to admire the calmness. Maybe it would be different this time, he thought, with the knowledge deep within that it wouldn't.","timestamp":convertTimestamp(time.time())})
        db.append("/notifications/notification",{"title":"She patiently waited for his number to be called. She had no desire to be there, but her mom had insisted that she go. She's resisted at first, but over time she realized it was simply easier to appease her and go. Mom tended to be that way. She would keep insisting until you wore down and did what she wanted. So, here she sat, patiently waiting for her number to be called.","timestamp":convertTimestamp(time.time())})
        db.append("/notifications/notification",{"title":"Patricia's friend who was here hardly had any issues at all, but she wasn't telling the truth. Yesterday, before she left to go home, she heard that her husband is in the hospital and pretended to be surprised. It later came out that she was the person who had put him there.","timestamp":convertTimestamp(time.time())})
        db.append("/turning",{"left":random.randint(0,101),"right":random.randint(0,101),"timestamp":convertTimestamp(time.time())})
        '''
        
        carCount = random.randint(0,51)
        truckCount = random.randint(0,51)
        total = carCount+truckCount
        db.append("/Traffic Data/TL001",{"car":carCount,"truck":truckCount,"Total":total,"timestamp":convertTimestamp(time.time())})
        sleep(5)
        carCount = random.randint(0,51)
        truckCount = random.randint(0,51)
        total = carCount+truckCount
        db.append("/Traffic Data/TL002",{"car":carCount,"truck":truckCount,"Total":total,"timestamp":convertTimestamp(time.time())})
        sleep(5)
        carCount = random.randint(0,51)
        truckCount = random.randint(0,51)
        total = carCount+truckCount
        db.append("/Traffic Data/TL003",{"car":carCount,"truck":truckCount,"Total":total,"timestamp":convertTimestamp(time.time())})
        sleep(5)
        
def push_fixed_notification(name,light_name,curr_status):
    if is_status_diff(name,light_name,curr_status):
        db.append("/Notifications/notification", {"unread": True, "title": f"Malfunctioned {name} {light_name.replace('_',' ')} has been fixed", "timestamp": convertTimestamp(time.time())})
        print("pushed fixed")
        
def is_status_diff(name,light_name,curr_status):
    print(light_name)
    prev_status = db.read(f"/TrafficLights/{name}/{light_name}")["status"]
    print(prev_status)
    return True if prev_status != curr_status else False

def push_malfunc_notification(name,light_name,curr_status):
    if is_status_diff(name,light_name,curr_status):
        db.append("/Notifications/notification", {"unread": True, "title": f"{name} {light_name.replace('_',' ')} has malfunctioned", "timestamp": convertTimestamp(time.time())})
        send_message(name,light_name)
        print("pushed malfunc")
        

def send_message(name,light_name):
    client = Client(account_sid, auth_token)
    message = client.messages \
            .create(
                body=f"{name} {light_name.replace('_',' ')} has malfunctioned",
                from_='+14752501567',
                to='+6011-11715229'
            )
    print(message.status)


main()

