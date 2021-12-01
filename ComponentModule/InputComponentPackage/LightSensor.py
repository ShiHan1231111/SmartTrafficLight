from ComponentModule.InputComponentPackage.InputComponent import InputComponent
from FakeDevices import *


class LightSensor(InputComponent):
    def __init__(self, pin_number):        
        super().__init__(pin_number)
        self.pin_number = pin_number

    def get_light_intensity(self):
        return str(analogRead(self.pin_number))
    
    def update(self,db):
        topic = f"light_{self.pin_number}"
        subtopics = ["light_intensity"]        
        subtopics_data = [self.get_light_intensity()]
        
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
