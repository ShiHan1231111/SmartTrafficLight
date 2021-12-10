from TrafficLight.TrafficLight import *
from grove_rgb_lcd import *
from Firebase import Firebase
from TrafficLight.EventListener import EventListener
from TrafficLight.EventAck import EventAck

import asyncio

ORDER = ["GREEN001", "RED001", "RED002"]
ID = "TL002"

redLight = 4
yellowLight = 3
greenLight = 2
checkRed = 7
checkYellow = 8
checkGreen = 5

TL = TrafficLight(ID, redLight, yellowLight, greenLight, checkRed, checkYellow, checkGreen)

fb = Firebase()
e = EventListener
ack = EventAck


def get_key(val, dict):
    for key, value in dict.items():
        if val == value:
            return key

    return "key doesn't exist"


async def sleepHalfSec():
    await asyncio.sleep(0.5)


async def main():
    while True:
        sleepTask = asyncio.create_task(sleepHalfSec())
        switchEvent = asyncio.create_task(e.listen_switch_event(ID))
        await asyncio.gather(sleepTask, switchEvent)
        switch = switchEvent.result()

        if switch == "SWITCH":
            current_display = get_key(ID, fb.access_by_path("Server/Order"))
            print(f"Current Display is {current_display}")
            if current_display == "GREEN001":
                red_transition_task = asyncio.create_task(red_transition())
                ackTask = asyncio.create_task(ack.ack_switch_event(ID))
                await asyncio.gather(red_transition_task, ackTask)
                print("CHECKING GREEN LIGHT")
                await check_green_light()

            elif current_display == "RED001":
                yellow_trans = asyncio.create_task(yellow_transition())
                yellow_check = asyncio.create_task(check_yellow_light(2))
                ackTask = asyncio.create_task(ack.ack_switch_event(ID))
                await asyncio.gather(yellow_trans, ackTask)
                await yellow_check

                start_red_and_off_yellow = asyncio.create_task(start_red())
                red_check = asyncio.create_task(check_red_light())
                await asyncio.gather(start_red_and_off_yellow, red_check)

            elif current_display == "RED002":
                print("OUTPUT LOG: TRANSITIONING.... RED001")
                sleep_task_ = asyncio.create_task(asyncio.sleep(3))
                on_red_task = asyncio.create_task(red_on())
                off_green_task = asyncio.create_task(green_off())
                ackTask = asyncio.create_task(ack.ack_switch_event(ID))
                await asyncio.gather(sleep_task_, ackTask, on_red_task)
                await check_red_light()
            else:
                print("The order is not valid error")
                # TODO: reset server table

        else:
            pass


async def red_transition():
    await asyncio.sleep(3)
    await asyncio.gather(green_on(), red_off())
    print("ACTION : ON GREEN....... OFF RED")


def switch_to_next_order(current_index):
    if current_index == 0 or current_index == 1:
        next_index = current_index + 1
    else:
        next_index = 0
    current_display = ORDER[next_index]
    return current_display


async def yellow_on():
    TL.yellowLight.turn_on()
    print("Displaying yellow..................")


async def yellow_off():
    TL.yellowLight.turn_off()
    print("Yellow is off......................")


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


async def check_green_light():
    await asyncio.sleep(0.00001)
    setRGB(0, 255, 0)
    while True:
        await asyncio.sleep(0.5)
        green_condition = TL.checkGreen.get_status()
        print(green_condition)
        if green_condition == 1:
            print("Green LED light has malfunctioned")
            TL.report_faulty_green()
            return False
        else:
            TL.green_light_ok()
            print("Green LED light is functioning")

        fetch_remaining_time_ = task_fetch_remaining_time()
        fetch_ambulance_data_ = task_fetch_ambulance_data()
        remaining_time, ambulance_data = await asyncio.gather(fetch_remaining_time_, fetch_ambulance_data_)
        have_ambulance = 'HAVE AMBULANCE' in ambulance_data.values()
        if have_ambulance:
            setText("Waiting for ambulance......")
        else:
            setText(f"Remaining time is {remaining_time}")

        try:
            if remaining_time <= 1:
                break
        except TypeError:
            break


async def check_red_light():
    await asyncio.sleep(0.00001)
    setRGB(255, 0, 0)
    while True:
        await asyncio.sleep(0.5)
        red_condition = TL.checkRed.get_status()
        print(red_condition)
        if red_condition == 1:
            print("Red LED light has malfunctioned")
            TL.report_faulty_red()
            return False
        else:
            TL.red_light_ok()
            print("Red LED light is functioning")

        fetch_remaining_time_ = task_fetch_remaining_time()
        fetch_ambulance_data_ = task_fetch_ambulance_data()
        remaining_time, ambulance_data = await asyncio.gather(fetch_remaining_time_, fetch_ambulance_data_)
        have_ambulance = 'HAVE AMBULANCE' in ambulance_data.values()
        if have_ambulance:
            setText("Waiting for ambulance......")
        else:
            setText(f"Remaining time is {remaining_time}")
        try:
            if remaining_time <= 1:
                break
        except TypeError:
            break


async def check_yellow_light(time_of_checking):
    await asyncio.sleep(0.00001)
    for loop_count in range(time_of_checking):
        await asyncio.sleep(1)
        setRGB(255, 165, 0)
        setText(f"Transitioning for {time_of_checking} second.........")
        yellow_condition = TL.checkYellow.get_status()
        print(yellow_condition)
        if yellow_condition == 1:
            print("Yellow LED Light has malfunctioned")
            TL.report_faulty_yellow()
            return False
        else:
            TL.yellow_light_ok()
            print("Yellow LED light is functioning")

        ambulance_data = await fetch_ambulance_data()
        have_ambulance = 'HAVE AMBULANCE' in ambulance_data.values()
        if have_ambulance:
            setText("Waiting for ambulance......")
        else:
            pass


async def fetch_ambulance_data():
    ambulance_data = fb.access_by_path("Server/Event/Ambulance")
    return ambulance_data


async def fetch_remaining_time():
    remaining_time = fb.access_by_path("Server/Time")
    return remaining_time


async def await_fetch_remaining_time():
    remaining_time = await fetch_remaining_time()
    return remaining_time


async def await_fetch_ambulance_data():
    ambulance_data = await fetch_ambulance_data()
    return ambulance_data


def task_fetch_ambulance_data():
    return asyncio.create_task(await_fetch_ambulance_data())


def task_fetch_remaining_time():
    return asyncio.create_task(await_fetch_remaining_time())


async def await_sleep(sleep_time):
    await asyncio.sleep(sleep_time)


def sleep_task(sleep_time):
    return asyncio.create_task(await_sleep(sleep_time))


async def yellow_transition():
    await asyncio.gather(yellow_on(), green_off())
    await asyncio.sleep(3)


async def start_red():
    await asyncio.gather(yellow_off(), red_on())


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
