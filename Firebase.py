import time

from pyrebase import pyrebase


class Firebase():
    def __init__(self):
        config = {
            "apiKey": "AIzaSyDekk741MySs8fpAVO_RkZqWD-lBOI_U2c",
            "authDomain": "smarttl-e6d87.firebaseapp.com",
            "databaseURL": "https://smarttl-e6d87-default-rtdb.asia-southeast1.firebasedatabase.app",
            "storageBucket": "smarttl-e6d87.appspot.com",
        }
        try:
            self.firebase = pyrebase.initialize_app(config)
            self.auth = self.firebase.auth()
            self.user = self.auth.sign_in_with_email_and_password("kchongee@gmail.com", "zt/h!\!*B;{)8/U$")
            self.db = self.firebase.database()
            self.storage = self.firebase.storage()
        except Exception as e:
            print(e)
            exit(-1)

            # datas can be any type of data (bool,num,dict,list)

    def replace(self, topic, datas):
        return self.db.child(topic).set(datas)

    # datas will be inserted under/inside a random generated key by firebase
    def append(self, topic, datas):
        return self.db.child(topic).push(datas)

    # datas must be 'dict' data type, insert to new under the topic and replace it if the key is existed
    def update(self, topic, datas):
        return self.db.child(topic).update(datas)

    def read(self, topic):
        return self.db.child(topic).get().val()

    def read_one(self, topic):
        return self.db.child(topic).get().val()

    def read_live(self, topic, stream_handler=None):
        if stream_handler is None:
            stream_handler = self._stream_handler
        return self.db.child(topic).stream(stream_handler)

    def _stream_handler(self, message):
        print(message["event"])
        print(message["path"])
        print(message["data"])

    def convert_timestamp(self, timestamp):
        return round(timestamp * 1000)

    def create_time_stamp(self):
        return self.convert_timestamp(time.time())

    def refresh_data(self):
        init_datas = {
            "notifications": {
                "unread": True,
                "notification": {
                    "timestamp1": "title(traffic_light1's light1 has malfunctioned)",
                    "timestamp2": "title(traffic_light2's light1 has malfunctioned)",
                },
            }
        }
        self.db.update("", init_datas)

    def remove_data(self, topic, key):
        return self.db.child(f"{topic}/{key}").remove()

    def access_by_path(self, topic):
        path_words = topic.split("/")
        data = self.db.child(path_words[0]).get().val()

        nest = dict(data)

        for i in range(len(path_words) - 1):
            nest = nest[path_words[i + 1]]
        return nest
