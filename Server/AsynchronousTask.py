import asyncio

from Server.ServerIO import *

io = ServerIO


class AsynchronousTask(object):
    @staticmethod
    def switch_tlight_order():
        return asyncio.create_task(switch_tlight_order())

    @staticmethod
    def update_tlight_to_switch_stat():
        return asyncio.create_task(io.update_all_to_switch())

    @staticmethod
    def reset_to_wait(order):
        return asyncio.create_task(reset_to_wait(order))

    @staticmethod
    async def async_print(text):
        return asyncio.create_task(await_async_print(text))

    @staticmethod
    def REQUEST_CAP(CAM_ID):
        return asyncio.create_task(REQUEST_CAP(CAM_ID))

    @staticmethod
    def obtain_cam_id(traffic_light_id):
        return asyncio.create_task(await_obtain_cam_id(traffic_light_id))

    @staticmethod
    def get_traffic_amount(order):
        return asyncio.create_task(await_get_traffic_data(order))

    @staticmethod
    def AKC_RECEIVED_TRAFFIC_DATA(order):
        return asyncio.create_task(await_ack_received(order))

    @staticmethod
    def update_transition():
        return asyncio.create_task(await_update_transition())

    @staticmethod
    def update_cycle_period(time):
        return asyncio.create_task(io.update_cycle_period(time))

    @staticmethod
    def read_ambulance_state_from_database():
        return asyncio.create_task(io.read_ambulance_state_from_database())

    @staticmethod
    def reset_ambulance_data():
        return asyncio.create_task(io.reset_ambulance_record())


async def await_async_print(text):
    await asynchronous_print(text)


async def asynchronous_print(text):
    print(text)


async def switch_tlight_order():
    old_order = io.get_tflight_order()
    cpy = old_order.copy()
    cpy["GREEN001"] = old_order["RED002"]
    cpy["RED001"] = old_order["GREEN001"]
    cpy["RED002"] = old_order["RED001"]
    new_order = cpy
    await io.update_tflight_order(new_order)
    return new_order


async def update_to_switch():
    await io.update_all_to_switch()


async def reset_to_wait(order):
    await io.WAITING(order)


async def REQUEST_CAP(CAM_ID):
    await io.REQUEST_CAP(CAM_ID)


async def obtain_cam_id(traffic_light_id):
    if traffic_light_id == "TL001":
        return "CM001"
    elif traffic_light_id == "TL002":
        return "CM002"
    else:
        return "CM003"


async def await_obtain_cam_id(traffic_light_id):
    x = await obtain_cam_id(traffic_light_id)
    return x


async def await_get_traffic_data(order):
    traffic_amt = await io.get_traffic_data(order)
    return traffic_amt


async def await_ack_received(order):
    await io.ACK_TRAFFIC_RECEIVE(order)


async def await_update_transition():
    await io.update_transitioning()
