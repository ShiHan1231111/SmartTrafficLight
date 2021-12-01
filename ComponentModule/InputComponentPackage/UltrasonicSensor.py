from datetime import datetime
from time import *
from ComponentModule.InputComponentPackage.InputComponent import InputComponent
from grovepi import *


class UltrasonicSensor(InputComponent):
    def __init__(self, pin_number):
        super().__init__(pin_number)

    def get_distance(self):
        return str(ultrasonicRead(self.pin_number))
    
    def update(self,db):            
        topic = f"ultrasonic_{self.pin_number}"
        subtopics = ["distance","jarak"]
        subtopics_data = [self.get_distance(),self.get_distance()]
        
        timestamp = round(time.time()*1000)
        datas = {}        
        if(len(subtopics) == len(subtopics_data)):
            for subtopic,subtopic_data in zip(subtopics,subtopics_data):            
                data = {
                    f"{subtopic}/{timestamp}": subtopic_data
                }
                datas.update(data)
        else:
            raise Exception("The subtopics and subtopics_data must have same length!")
        
        #print(datas)                
        db.child(topic).update(datas)
