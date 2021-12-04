import asyncio
import time
from asyncio import sleep

from Firebase import Firebase

firebase = Firebase()


# value1 = firebase.read_one("Testing/Controller")

# wait time == need other work? = > yes become independent function | what? => run the loop
# depender :
async def waiting_time_for_controller_change():
    val1 = firebase.read_one("Testing/Controller")
    val2 = val1
    while True:
        val1 = firebase.read_one("Testing/Controller")
        await asyncio.sleep(1)  # Other action
        if val2 != val1:
            return True


# receiver
async def receive_update_message_time_sharer():
    print("waiting update message.........")
    msg = await waiting_time_for_controller_change()
    print(f"received update msg {msg}")
    return msg


# wait time == need other work? = > yes become independent function | what? => recieve the update when wait
async def waiting_time_for_sleeper():
    await asyncio.sleep(5)
    return True


async def receive_finish_sleep_time_sharer():
    print("starting to sleep....")
    msg = await waiting_time_for_sleeper()
    return msg


async def main():

    while True:
        receive_update = asyncio.create_task(receive_update_message_time_sharer())
        done_sleep = asyncio.create_task(receive_finish_sleep_time_sharer())
        await receive_update
        await done_sleep


asyncio.run(main())
