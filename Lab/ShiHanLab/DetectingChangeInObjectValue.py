import asyncio
from Firebase import Firebase

FB = Firebase()


class Flag(object):
    def __init__(self):
        self._control_flag = FB.read_one("Testing/Controller")

    async def get_sleep_4_task(self, val):
        print(f"displaying.........{val}")
        return asyncio.create_task(await asyncio.sleep(4))

    "MECHANISM OF DETECTION, keepp update into"

    @property
    async def control_flag(self):
        return self._control_flag

    @control_flag.setter
    async def control_flag(self, control_flag):
        task = self.get_sleep_4_task(FB.read_one("Testing/Controller"))
        val = FB.read_one("Testing/Controller")
        await task
        if self._control_flag != val:
            self._control_flag = val
            await killTask(task)
            await self.get_sleep_4_task(self._control_flag)


async def tester():
    while True:
        await observe_update()
        await asyncio.sleep(0.2)  # JMP next coroutine


async def killTask(task):
    task.cancel()


async def observe_update():
    cf = Flag()
    cf.control_flag = FB.read_one("Testing/Controller")


asyncio.run(tester())
