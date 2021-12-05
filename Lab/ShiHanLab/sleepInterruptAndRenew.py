import asyncio
import time

from Firebase import Firebase

FB = Firebase()
val1 = FB.read_one("Testing/Controller")

async def sleep6():
    await asyncio.sleep(6)
    return True


async def detect_flag_change():
    val2 = FB.read_one("Testing/Controller")


await sleep6
await detect_flag_change
await sleepIsDone
await killAllTask
