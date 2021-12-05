from Firebase import Firebase

fb = Firebase()


class ServerIO(object):
    @staticmethod
    def get_tflight_order():
        return fb.read("Server/Order")

    @staticmethod
    def update_tflight_order(new_order):
        fb.update("Server/Order", new_order)
