import asyncio
from AsynchronousTask import *

asynT = AsynchronousTask
io = ServerIO


async def event_loop():
    while True:
        print("restarting..........")
        for i in range(5):
            await asyncio.sleep(1)
        await asyncio.gather(io.update_all_to_switch(),asynT.switch_tlight_order())
        await asyncio.sleep(5)


asyncio.run(event_loop())
