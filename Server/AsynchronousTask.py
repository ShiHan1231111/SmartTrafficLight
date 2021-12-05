import asyncio

from Server.SynchronousTask import SynchronousTask

synT = SynchronousTask


async def wait_and_switch_order(time):
    await asyncio.sleep(time)
    synT.switch_tlight_order()


class AsynchronousTask(object):
    pass
