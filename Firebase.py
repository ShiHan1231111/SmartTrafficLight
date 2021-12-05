from pyrebase import pyrebase

class Firebase():
    def __init__(self):
        config = {
            "apiKey":"AIzaSyDGGWQfuvSiiCPpL2MUIJi1HO_TdmscVlY",
            "authDomain":"bait2123-iot-b0887.firebaseapp.com",
            "databaseURL":"https://bait2123-iot-b0887-default-rtdb.asia-southeast1.firebasedatabase.app/",
            "storageBucket":"gs://bait2123-iot-b0887.appspot.com",
        }
        try:
            self.firebase = pyrebase.initialize_app(config)
            self.auth = self.firebase.auth()
            self.user = self.auth.sign_in_with_email_and_password("kchongee@gmail.com","zt/h!\!*B;{)8/U$")
            self.db = self.firebase.database()
            self.storage = self.firebase.storage()
        except Exception as e:
            print(e)
            exit(-1)            
    
    # datas can be any type of data (bool,num,dict,list)
    def replace(self,topic,datas):        
        return self.db.child(topic).set(datas)
    
    # datas will be inserted under/inside a random generated key by firebase
    def append(self,topic,datas):        
        return self.db.child(topic).push(datas)
        
    # datas must be 'dict' data type, insert to new under the topic and replace it if the key is existed
    def update(self,topic,datas):        
        return self.db.child(topic).update(datas)
        
    def read(self,topic):        
        return self.db.child(topic).get().val()
        
    def read_one(self,topic):
        return self.db.child(topic).get().val()
        
            
    def read_live(self,topic,stream_handler = None):
        if stream_handler is None:
            stream_handler = self._stream_handler
        return self.db.child(topic).stream(stream_handler)

    def _stream_handler(self,message):
        print(message["event"])
        print(message["path"])
        print(message["data"])

    def refresh_data(self):
        init_datas = {
            "roads":{
                    "road1":{
                            "timestamp": 0
                        },
                    "road2":{
                            "timestamp": 0
                        },
                    "road3":{
                            "timestamp": 0
                        }
                },
            "traffic_lights":{
                    "order":[
                            "traffic_light1",
                            "traffic_light2",
                            "traffic_light3",
                        ],
                    "have_ambulance": "",
                    "interrupted":{
                            "traffic_light": "",
                            "remaining_seconds": ""
                        },
                    "traffic_light1":{
                            "light1":{
                                "status":"flawless",
                                "date_mulfunctioned":"timestamp"                                
                                },
                            "light2":{
                                "status":"flawless",
                                "date_mulfunctioned":"timestamp"                                
                                },
                            "light3":{
                                "status":"flawless",
                                "date_mulfunctioned":"timestamp"                                
                                },
                        },
                    "traffic_light2":{
                            "light1":{
                                "status":"flawless",
                                "date_mulfunctioned":"timestamp"                                
                                },
                            "light2":{
                                "status":"flawless",
                                "date_mulfunctioned":"timestamp"                                
                                },
                            "light3":{
                                "status":"flawless",
                                "date_mulfunctioned":"timestamp"                                
                                },
                        },
                    "traffic_light3":{
                            "light1":{
                                "status":"flawless",
                                "date_mulfunctioned":"timestamp"                                
                                },
                            "light2":{
                                "status":"flawless",
                                "date_mulfunctioned":"timestamp"                                
                                },
                            "light3":{
                                "status":"flawless",
                                "date_mulfunctioned":"timestamp"                                
                                },                            
                        },
                },
            "ambulance":{
                    "traffic_light1":[
                            "timestamp",
                            "timestamp",
                        ],
                    "traffic_light2":[
                            "timestamp",
                            "timestamp",
                        ],
                    "traffic_light3":[
                            "timestamp",
                            "timestamp",
                        ]
                },
            "notifications":{
                    "unread": True,
                    "notification": {
                            "timestamp1": "title(traffic_light1's light1 was mulfunctioned)",
                            "timestamp2": "title(traffic_light2's light1 was mulfunctioned)",
                        },                                                    
                }
        }    
        self.db.update("",init_datas)


    def remove_data(self,topic,key):
        return self.db.child(f"{topic}/{key}").remove()

        