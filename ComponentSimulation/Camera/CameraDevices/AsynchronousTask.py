import asyncio

from ComponentSimulation.Camera.CameraDevices.CapIO import *

io = CapIO


class AsynT(object):
    @staticmethod
    def sleep(time):
        return asyncio.create_task(asyncio.sleep(time))

    @staticmethod
    def listen_capture_event(CAM_ID):
        return asyncio.create_task(listen_capture_event(CAM_ID))

    @staticmethod
    def CAP_ACK(CAM_ID):
        return asyncio.create_task(CAP_ACK(CAM_ID))

    @staticmethod
    def capture_img(directory, filename):
        return asyncio.create_task(capture_img(directory, filename))

    @staticmethod
    def update_traffic(order, amount):
        return asyncio.create_task(update_traffic(order, amount))

    @staticmethod
    def update_traffic_data(complete_dict_with_timestamp, TLID):
        return asyncio.create_task(io.append_traffic_data(complete_dict_with_timestamp, TLID))

    @staticmethod
    def reset_waiting_state(order):
        return asyncio.create_task(order)


async def listen_capture_event(CAM_ID):
    event = await io.listen_cap_event(CAM_ID)
    return event


async def CAP_ACK(CAM_ID):
    await io.ack_cap(CAM_ID)


async def capture_img(directory, filename):
    img = await io.capture_image(directory, filename)
    return img


async def update_traffic(order, amount):
    await io.update_traffic_amount(order, amount)


async def append_traffic_data(TLID, key, complete_dict):
    await io.append_traffic_data(TLID, key, complete_dict)
