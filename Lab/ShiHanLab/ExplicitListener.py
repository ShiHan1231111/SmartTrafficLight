import asyncio

from pyasn1.compat.octets import null

from Firebase import Firebase

fb = Firebase()

globalFlag = -1


class detect_change(object):
    def __init__(self):
        self.currentTask = null
        self.controller = fb.read_one("Testing/Controller")

    def get_controller(self):
        return self.controller

    async def set_controller(self, val):
        global globalFlag
        if self.get_controller() != val:
            globalFlag = 1
            self.controller = val
            print(f"value updated to {val}")
            self.currentTask = get_sleep4_task(val)
            await self.currentTask
        else:
            globalFlag = 0


async def sleep_4_task():
    print("started the loop")
    await asyncio.sleep(4)
    print("ended the loop")


def get_sleep4_task(val):
    print(f"running...with {val}")
    return asyncio.create_task(sleep_4_task())


async def kll_task_if_updated(task):
    global globalFlag
    if globalFlag == 1:
        task.cancel()


async def main():
    detector = detect_change()
    while True:
        await asyncio.sleep(0.2)
        await kll_task_if_updated(detector.currentTask)
        await detector.set_controller(fb.read_one("Testing/Controller"))

asyncio.run(main())
