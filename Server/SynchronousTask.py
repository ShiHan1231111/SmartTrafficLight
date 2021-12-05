from Server.ServerIO import ServerIO

io = ServerIO


class SynchronousTask(object):
    @staticmethod
    def switch_tlight_order():
        old_order = io.get_tflight_order()
        cpy = old_order.copy()
        cpy["GREEN001"] = old_order["RED002"]
        cpy["RED001"] = old_order["GREEN001"]
        cpy["RED002"] = old_order["RED001"]
        new_order = cpy
        io.update_tflight_order(new_order)

