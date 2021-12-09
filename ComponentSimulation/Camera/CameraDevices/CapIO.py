import os.path

from cv2 import cv2
from Firebase import Firebase

fb = Firebase()


class CapIO(object):
    @staticmethod
    async def listen_cap_event(CAM_ID):
        event = fb.access_by_path(f"Server/Event/Capture/{CAM_ID}")
        return event

    @staticmethod
    async def ack_cap(CAM_ID):
        fb.update(f"Server/Event/Capture", {f"{CAM_ID}": "CAP_ACK"})

    @staticmethod
    async def capture_image(directory, filename):
        return cv2.imread(os.path.join(directory, filename))
        # NOTE: uncomment below code & delete above code, if realtime
        # cap = cv2.VideoCapture(0)
        # ret,frame = cap.read()
        # return frame

    @staticmethod
    def get_order(traffic_light_id):
        order_dict = fb.access_by_path("Server/Order")
        return get_key(traffic_light_id, order_dict)

    @staticmethod
    async def update_traffic_amount(order, amount):
        fb.update("Server/TrafficAmount", {order: amount})

    @staticmethod
    async def append_traffic_data(key, complete_dict, TLID):
        fb.update(f"Traffic Data/{TLID}", {key: complete_dict})


def get_key(val, dict):
    for key, value in dict.items():
        if val == value:
            return key
