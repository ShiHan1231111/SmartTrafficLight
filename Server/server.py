import asyncio
from Firebase import Firebase
from Server import AsynchronousTask, SynchronousTask
from Server.ServerIO import ServerIO

asynT = AsynchronousTask
synT = SynchronousTask
io = ServerIO


async def wait_and_switch():
    await asyncio.gather(*[asynT.wait_and_switch_order(8)])


async def event_loop():
    while True:
        for i in range(5):
            print("restarting..........")
            await asyncio.sleep(1)
        io.update_all_to_switch()
        await asyncio.sleep(5)


asyncio.run(event_loop())
