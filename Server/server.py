import asyncio

from Server.AsynchronousTask import *

asynT = AsynchronousTask
STANDARD_PERIOD = 9
intelli_period = 9


async def event_loop():
    global intelli_period
    transition_period = 3
    order = dict(io.get_tflight_order())
    TFID_RED001, TFID_RED002 = order["RED001"], order['RED002']
    while True:

        fb.update("Server/TrafficAmount", {"RED001": "20"})
        fb.update("Server/TrafficAmount", {"RED002": "30"})

        # Reinitialize value
        print("NEW CYCLE")
        red001_traffic, red002_traffic = "WAITING", "WAITING"
        is_required_compare = True
        is_required_read = True

        CAM_ID1, CAM_ID2 = await asyncio.gather(
            asynT.obtain_cam_id(TFID_RED001),
            asynT.obtain_cam_id(TFID_RED002))

        for i in range(intelli_period):
            await count_down(i)

            remaining_time = intelli_period - i

            if is_time_to_capture(remaining_time, 8):
                await reset_database_and_request_cap(CAM_ID1, CAM_ID2)
                fb.update("Server/TrafficAmount", {"RED001": "20"})
                fb.update("Server/TrafficAmount", {"RED002": "30"})

            if remaining_time < 8:

                if no_data_fetched(red001_traffic, red002_traffic) and is_required_read:
                    red001_traffic, red002_traffic = await continue_fetch_traffic_data()

                if all_data_fetched(red001_traffic, red002_traffic) and is_required_compare:
                    TFFC_RED001 = red001_traffic
                    TFFC_RED002 = red002_traffic
                    is_required_compare = False
                    is_required_read = False
                    await acknowledge_both_registry()

                if only_road1_data_is_fetched(red001_traffic, red002_traffic):
                    await asynT.AKC_RECEIVED_TRAFFIC_DATA("RED001")

                if only_road2_data_is_fetched(red001_traffic, red002_traffic):
                    await asynT.AKC_RECEIVED_TRAFFIC_DATA("RED002")

                else:
                    # DEFAULT VALUE WHEN MALFUNCTION OCCUR
                    TFFC_RED001 = 10
                    TFFC_RED002 = 10

        # out side the loop
        if both_roads_have_no_car(TFFC_RED001, TFFC_RED002):
            await proceed_without_switch(transition_period)
            intelli_period = STANDARD_PERIOD

        elif road1_have_no_car_but_road2_have(TFFC_RED001, TFFC_RED002):
            order = await skip_road1_green_turn()
            order = dict(order)
            TFID_RED001, TFID_RED002 = order['RED001'], order['RED002']  # Help to identify camera id
            intelli_period = STANDARD_PERIOD
            await display_transition(transition_period)

        elif both_side_is_almost_equal_or_road2_no_car(TFFC_RED001, TFFC_RED002, 6):
            order = await switch_road1_to_green()
            order = dict(order)
            TFID_RED001, TFID_RED002 = order['RED001'], order['RED002']  # Help to identify camera id
            intelli_period = STANDARD_PERIOD
            await display_transition(transition_period)

        elif red001_traffic > red002_traffic:
            percentage = red002_traffic / red001_traffic
            print(percentage)
            intelli_period = STANDARD_PERIOD * percentage
            await asynT.update_cycle_period(intelli_period)
            await switch_road1_to_green()
            await display_transition(transition_period)
        await asynT.update_cycle_period(intelli_period)


async def reset_database_and_request_cap(CAM_ID1, CAM_ID2):
    await asyncio.gather(
        asynT.reset_to_wait("RED001"),
        asynT.reset_to_wait("RED002"),
        asynT.REQUEST_CAP(CAM_ID1),
        asynT.REQUEST_CAP(CAM_ID2))


async def count_down(i):
    await asyncio.gather(asyncio.sleep(1), io.update_time(intelli_period - i))


def is_time_to_capture(i, remaining_time):
    return i == remaining_time


def no_data_fetched(red001_traffic, red002_traffic):
    return red001_traffic == "WAITING" or red002_traffic == "WAITING"


async def continue_fetch_traffic_data():
    x = asynT.get_traffic_amount("RED001")
    y = asynT.get_traffic_amount("RED002")
    return await asyncio.gather(x, y)


def all_data_fetched(red001_traffic, red002_traffic):
    return red001_traffic != "WAITING" and red002_traffic != "WAITING"


def only_road1_data_is_fetched(red001_traffic, red002_traffic):
    return red001_traffic != "WAITING" and red002_traffic == "WAITING"


def only_road2_data_is_fetched(red001_traffic, red002_traffic):
    return red002_traffic != "WAITING" and red001_traffic == "WAITING"


async def acknowledge_both_registry():
    await asyncio.gather(
        asynT.AKC_RECEIVED_TRAFFIC_DATA("RED001"),
        asynT.AKC_RECEIVED_TRAFFIC_DATA("RED002"))


def both_roads_have_no_car(TFFC_RED002, TFFC_RED001):
    return TFFC_RED002 == 0 and TFFC_RED001 == 0


async def proceed_without_switch(transition_period):
    await asyncio.gather(
        asynT.async_print("Proceed without switch"),
        asynT.async_print(f"{transition_period} sec transition....."),
        asynT.update_transition(),
        asyncio.sleep(transition_period))


async def display_transition(transition_period):
    await proceed_without_switch(transition_period)


def road1_have_no_car_but_road2_have(TFFC_RED001, TFFC_RED002):
    return TFFC_RED001 == 0 and TFFC_RED002 > 0


async def skip_road1_green_turn():
    for i in range(2):
        _, new_order = \
            await asyncio.gather(
                asynT.update_tlight_to_switch_stat(),
                asynT.switch_tlight_order())
    return new_order


def both_side_is_almost_equal_or_road2_no_car(TFFC_RED001, TFFC_RED002, difference_between_two_road):
    return (abs(TFFC_RED001 - TFFC_RED002) <= difference_between_two_road) or (TFFC_RED002 == 0 and TFFC_RED001 != 0)


async def switch_road1_to_green():
    _, new_order = \
        await asyncio.gather(
            asynT.update_tlight_to_switch_stat(),
            asynT.switch_tlight_order())
    return new_order


def start_ambulance_cycle():

    pass


asyncio.run(event_loop())
