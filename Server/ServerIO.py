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
        fb.update("Server", {"Time": "Transition...."})

    @staticmethod
    async def update_cycle_period(period):
        fb.update("Server", {"StaticPeriod": period})

    @staticmethod
    async def read_ambulance_state_from_database():
        return fb.access_by_path("Server/Event/Ambulance")

    @staticmethod
    async def reset_ambulance_record():
        initial_ambulance_data = {
            "IS PASS": "NOT PASSED",
            "TL001": "NO AMBULANCE",
            "TL002": "NO AMBULANCE",
            "TL003": "NO AMBULANCE"
        }
        fb.update("Server/Event", {"Ambulance": initial_ambulance_data})

    @staticmethod
    async def read_ambulance_have_pass_flag():
        return fb.access_by_path("Server/Event/Ambulance/IS PASS")

    @staticmethod
    async def reset_back_is_pass_flag_to_no_ambulance():
        fb.update("Server/Event/Ambulance", {"IS PASS": "HAVE PASSED"})

    @staticmethod
    async def resume_the_traffic_light_to_previous_order(PREVIOUS_ORDER):
        fb.update("Server", {"Order":PREVIOUS_ORDER})

    @staticmethod
    async def switch_to_ambulance_priority_order(PROPER_AMBULANCE_ORDER):
        fb.update("Server", {"Order": PROPER_AMBULANCE_ORDER})


