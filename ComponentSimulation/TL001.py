from TrafficLight.TrafficLight import *
import asyncio
from grove_rgb_lcd import *
from ComponentSimulation.Firebase import Firebase

ORDER = ["GREEN001", "RED001", "RED002"]
ID = "TL001"

redLight = 2
yellowLight = 3
greenLight = 4

checkRed = 5
checkYellow = 6
checkGreen = 7

TL = TrafficLight(ID, redLight, yellowLight, greenLight, checkRed, checkYellow, checkGreen)


class EventListener:
    @staticmethod
    async def listen_switch_event():
        switch_instruction = await listen_switch()
        return switch_instruction


async def listen_switch():
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
    while True:
        sleepTask = asyncio.create_task(sleepHalfSec())
        switchEvent = asyncio.create_task(e.listen_switch_event())
        await asyncio.gather(sleepTask, switchEvent)

        switch = switchEvent.result()

        if switch == "SWITCH" and current_display == "GREEN001":
            TL.redLight.turn_off()
            print("red Turned off............")
            yellowTask = asyncio.create_task(yellow_transition())
            yellow_check = asyncio.create_task(check_yellow_light())
            ackTask = asyncio.create_task(ack.ack_switch_event())


            await asyncio.gather(yellowTask, ackTask, yellow_check)
            await asyncio.gather(yellowTask, ackTask, yellow_check)
            switch_to_next_order(ORDER.index(current_display))
            await indicating_display()

        elif switch == "SWITCH" and current_display != "GREEN001":
            redTask = asyncio.create_task(red_transition())
            ackTask = asyncio.create_task(ack.ack_switch_event())

            await asyncio.gather(redTask, ackTask)
            switch_to_next_order(ORDER.index(current_display))
            await indicating_display()

        else:
            pass


async def yellow_transition():
    TL.greenLight.turn_off()
    TL.yellowLight.turn_on()
    await asyncio.sleep(3)
    TL.yellowLight.turn_off()


async def check_yellow_light():
    count = 3
    await asyncio.sleep(0.00001)
    for loop_count in range(3):
        setRGB(255, 165, 0)
        setText("Time Remaining: \n" + str(count) + " seconds")
        count -= 1
        yellow_condition = TL.checkYellow.get_status()
        if yellow_condition == 1:
            TL.report_faulty_yellow()
            return False
        else:
            print("Yellow LED light is functioning")
        await asyncio.sleep(1)
    return True


async def red_transition():
    await asyncio.sleep(3)
    TL.redLight.turn_off()


def switch_to_next_order(current_index):
    global current_display
    if current_index == 0 or current_index == 1:
        next_index = current_index + 1
    else:
        next_index = 0
    current_display = ORDER[next_index]


async def indicating_display():
    if current_display == "GREEN001":
        green_task = asyncio.create_task(green_on())
        green_check = asyncio.create_task(check_green_light("SWITCH"))
        await asyncio.gather(green_task, green_check)
    else:
        red_task = asyncio.create_task(red_on())
        red_check = asyncio.create_task(check_red_light("SWITCH"))
        await asyncio.gather(red_task, red_check)


async def green_on():
    print("Displaying green...................................")
    TL.greenLight.turn_on()


async def green_off():
    print("Turn off green......................................")
    TL.greenLight.turn_off()


async def red_on():
    print("Displaying red................................")
    TL.redLight.turn_on()


async def red_off():
    print("turn off red..................................")
    TL.redLight.turn_off()


async def check_green_light(switch_instruction):
    await asyncio.sleep(0.00001)
    while True:
        if switch_instruction == "SWITCH":
            break
        else:
            setRGB(0, 255, 0)
            await asyncio.gather(sleep_task(1), display_on_lcd())
            green_condition = TL.checkGreen.get_status()
            if green_condition == 1:
                TL.report_faulty_green()
                return False
            else:
                print("Green LED light is functioning")
        await asyncio.sleep(1)
    return True


async def red_on_off(switch_instruction):
    TL.redLight.turn_on()
    if switch_instruction == "SWITCH":
        TL.redLight.turn_off()


async def check_red_light(switch_instruction):
    await asyncio.sleep(0.00001)
    while True:
        if switch_instruction == "SWITCH":
            break
        else:
            setRGB(255, 0, 0)
            await asyncio.gather(sleep_task(1), display_on_lcd())
            green_condition = TL.checkGreen.get_status()
            if green_condition == 1:
                TL.report_faulty_red()
                return False
            else:
                print("Red LED light is functioning")
        await asyncio.sleep(1)
    return True


async def await_sleep(sleep_time):
    await asyncio.sleep(sleep_time)


def sleep_task(sleep_time):
    return asyncio.create_task(await_sleep(sleep_time))


async def display_on_lcd():
    count = await get_remaining_time()
    setText(f"Time Remaining: \n" + str(count) + " seconds")


async def get_remaining_time():
    return fb.access_by_path("Server/Time")


'''
async def check_red_light(red_time):
    count = red_time
    for loop_count in range(red_time):
        await asyncio.sleep(0.00001)
        setRGB(255, 0, 0)
        setText("Red Light: \n"+str(count)+" seconds")
        count -= 1
        red_condition = TL.checkRed.get_status()
        if red_condition == 1:
            TL.report_faulty_red()
            return False
        else:
            print("Red LED light is functioning")
        await asyncio.sleep(1)
    return True
'''

asyncio.run(main())
