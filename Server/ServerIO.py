from Firebase import Firebase

fb = Firebase()


class ServerIO(object):
    @staticmethod
    def get_tflight_order():
        return fb.read("Server/Order")

    @staticmethod
    async def update_tflight_order(new_order):
        fb.update("Server/Order", new_order)

    @staticmethod
    async def update_all_to_switch():
        data = {"TL001": "SWITCH",
                "TL002": "SWITCH",
                "TL003": "SWITCH"}
        fb.update("Server/Event/Switch", data)

    @staticmethod
    async def update_time(time):
        fb.update("Server", {"Time": time})

    @staticmethod
    async def REQUEST_CAP(CAM_ID):
        fb.update("Server/Event/Capture", {str(CAM_ID): "REQUEST_CAP"})

    @staticmethod
    async def ACK_TRAFFIC_RECEIVE(order):
        fb.update("Server/TrafficAmount", {order: "ACK DATA RECEIVE"})

    @staticmethod
    async def WAITING(order):
        fb.update("Server/TrafficAmount", {order: "WAITING"})

    @staticmethod
    async def get_traffic_data(order):
        traffic_amount = fb.access_by_path(f"Server/TrafficAmount/{order}")
        return traffic_amount

    @staticmethod
    async def update_transitioning():
        fb.update("Server",{"Time":"Transition...."})
