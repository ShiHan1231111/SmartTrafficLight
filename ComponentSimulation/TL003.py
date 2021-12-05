import asyncio

from Firebase import Firebase

ORDER = ["GREEN001", "RED001", "RED002"]
ID = "TL003"


class EventListener:
    @staticmethod
    async def listen_switch_event():
        switch_instructio = await listen_swith()
        return switch_instructio


async def listen_swith():
    return fb.read_one(f"Server/Event/Switch/{ID}")


class EventAck(object):
    @staticmethod
    async def ack_switch_event():
        await EventAck.send_switch_ack()

    @staticmethod
    async def send_switch_ack():
        fb.update("Server/Event/Switch", {ID: "SWITCH ACK"})


fb = Firebase()
e = EventListener
ack = EventAck


def get_key(val, dict):
    for key, value in dict.items():
        if val == value:
            return key

    return "key doesn't exist"


current_display = get_key(ID, fb.access_by_path("Server/Order"))


async def sleepHalfSec():
    await asyncio.sleep(0.5)


async def main():
    indicating_display()
    while True:

        sleepTask = asyncio.create_task(sleepHalfSec())
        switchEvent = asyncio.create_task(e.listen_switch_event())
        await asyncio.gather(sleepTask, switchEvent)

        switch = switchEvent.result()

        if switch == "SWITCH" and current_display == "GREEN001":
            print("Turning yellow..........")
            yellowTask = asyncio.create_task(yellow_transition())
            ackTask = asyncio.create_task(ack.ack_switch_event())
            await asyncio.gather(yellowTask, ackTask)
            switch_to_next_order(ORDER.index(current_display))
            indicating_display()

        elif switch == "SWITCH" and current_display != "GREEN001":
            redTask = asyncio.create_task(red_transition())
            ackTask = asyncio.create_task(ack.ack_switch_event())
            await asyncio.gather(redTask, ackTask)
            switch_to_next_order(ORDER.index(current_display))
            indicating_display()

        else:
            pass


async def yellow_transition():
    await asyncio.sleep(5)


async def red_transition():
    await asyncio.sleep(5)


def switch_to_next_order(current_index):
    global current_display
    if current_index == 0 or current_index == 1:
        next_index = current_index + 1
    else:
        next_index = 0
    current_display = ORDER[next_index]



def indicating_display():
    if current_display == "GREEN001":
        print("Displaying Green............")
    else:
        print("Displaying Red..............")


asyncio.run(main())
