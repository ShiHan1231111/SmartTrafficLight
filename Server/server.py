import asyncio
from Firebase import Firebase
from Server import AsynchronousTask, SynchronousTask

asynT = AsynchronousTask
synT = SynchronousTask


async def main():
    await asyncio.gather(*[asynT.wait_and_switch_order(5)])

while True:
    print("restarting..........")
    asyncio.run(main())