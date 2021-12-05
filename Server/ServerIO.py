from Firebase import Firebase

fb = Firebase()


class ServerIO(object):
    @staticmethod
    def get_tflight_order():
        return fb.read("Server/Order")

    @staticmethod
    def update_tflight_order(new_order):
        fb.update("Server/Order", new_order)

    @staticmethod
    def update_all_to_switch():
        data = {"TL001": "SWITCH",
                "TL002": "SWITCH",
                "TL003": "SWITCH"}
        fb.update("Server/Event/Switch",data)
