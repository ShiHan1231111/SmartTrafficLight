import asyncio

import Server.AsynchronousTask as asynT


async def testing():
    await asyncio.gather(
        asynT.update_tlight_to_switch_stat(),
        asynT.switch_tlight_order())


asyncio.run(testing())
