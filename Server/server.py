import asyncio

from Server.AsynchronousTask import *

asynT = AsynchronousTask
STANDARD_PERIOD = 10
intelli_period = 10


async def event_loop():
    global intelli_period
    transition_period = 3
    order = dict(io.get_tflight_order())
    TFID_RED001, TFID_RED002 = order["RED001"], order['RED002']
    while True:

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

            if remaining_time < 8:

                fb.update("Server/TrafficAmount", {"RED001": "0"})
                fb.update("Server/TrafficAmount", {"RED002": "40"})

                if no_data_fetched(red001_traffic, red002_traffic) and is_required_read:
                    print("LOGIC LOG : NO DATA FETCHED")
                    red001_traffic, red002_traffic = await continue_fetch_traffic_data()

                elif all_data_fetched(red001_traffic, red002_traffic) and is_required_compare:
                    print("LOGIC LOG : ALL DATA FETCHED")
                    TFFC_RED001 = red001_traffic
                    TFFC_RED002 = red002_traffic
                    is_required_compare = False
                    is_required_read = False
                    await acknowledge_both_registry()

                elif only_road1_data_is_fetched(red001_traffic, red002_traffic) and is_required_compare:
                    print("LOGIC LOG : ONLY_ROAD1_DATA_IS_FETCHED")
                    await asynT.AKC_RECEIVED_TRAFFIC_DATA("RED001")

                elif only_road2_data_is_fetched(red001_traffic, red002_traffic):
                    print("LOGIC LOG : ONLY_ROAD2_DATA_IS_FETCHED")
                    await asynT.AKC_RECEIVED_TRAFFIC_DATA("RED002")

                else:
                    pass

        # out side the loop
        try:
            TFFC_RED001 = int(TFFC_RED001)
            TFFC_RED002 = int(TFFC_RED002)
        except TypeError:
            print("ERROR: CAM MIGHT FAULTY")

        print(f"MONITOR TRAFFIC LOG: RED001 traffic is {TFFC_RED001}")
        print(f"MONITOR TRAFFIC LOG: RED002 traffic is {TFFC_RED002}")

        if both_roads_have_no_car(TFFC_RED001, TFFC_RED002):
            intelli_period = STANDARD_PERIOD
            await asynT.update_cycle_period(intelli_period)
            print("LOGIC LOG : DETECTED BOTH ROAD NO CAR")
            await proceed_without_switch(transition_period)

        elif road1_have_no_car_but_road2_have(TFFC_RED001, TFFC_RED002):
            intelli_period = STANDARD_PERIOD
            await asynT.update_cycle_period(intelli_period)
            print("LOGIC LOG : ROAD1_HAVE_NO_CAR_BUT_ROAD2_HAVE")
            order = await skip_road1_green_turn()
            await display_transition(transition_period)
            order = dict(order)
            TFID_RED001, TFID_RED002 = order['RED001'], order['RED002']  # Help to identify camera id

        elif both_side_is_almost_equal_or_road2_no_car(TFFC_RED001, TFFC_RED002, 6):
            print("both_side_is_almost_equal_or_road2_no_car")
            intelli_period = STANDARD_PERIOD
            await asynT.update_cycle_period(intelli_period)
            order = await switch_road1_to_green()
            await display_transition(transition_period)
            order = dict(order)
            TFID_RED001, TFID_RED002 = order['RED001'], order['RED002']  # Help to identify camera id
            intelli_period = STANDARD_PERIOD

        elif red001_traffic > red002_traffic:
            print("LOGIC LOG : DETECTED RED001_TRAFFIC > RED002_TRAFFIC")
            percentage = 1 + ((TFFC_RED001 - TFFC_RED002) / TFFC_RED001)
            print(f"OUTPUT LOG: Percentage IS {percentage}%")
            intelli_period = round(STANDARD_PERIOD * percentage)
            print(f"OUTPUT LOG: intelli_period IS {intelli_period}")
            await asynT.update_cycle_period(intelli_period)
            await switch_road1_to_green()
            await display_transition(transition_period)

        elif red001_traffic < red002_traffic:
            print("LOGIC LOG : DETECTED red001_traffic < red002_traffic")
            order = await switch_road1_to_green()
            await display_transition(transition_period)
            order = dict(order)
            TFID_RED001, TFID_RED002 = order['RED001'], order['RED002']  # Help to identify camera id
            intelli_period = STANDARD_PERIOD
            pass

        else:
            print("ERROR OCCURRED, AI OR CAM MODULE MIGHT MALFUNCTION")
            pass

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
    return red001_traffic != "WAITING" and red002_traffic != "WAITING" \
           and red001_traffic != "ACK DATA RECEIVE" and red002_traffic != "ACK DATA RECEIVE"


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
        asynT.async_print("ACTION LOG: Switch without switching"),
        display_transition(transition_period))


async def display_transition(transition_period):
    taskA = asynT.async_print(f"{transition_period} sec transition.....")
    taskB = asynT.update_transition()
    await asyncio.gather(taskA, taskB)


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


def get_key(target_value, dictionary):
    for key, value in dictionary.items():
        if target_value == value:
            return key

    return "key doesn't exist"


def start_ambulance_cycle():
    ambulance_data = await asynT.read_ambulance_state_from_database()
    have_ambulance = 'HAVE AMBULANCE' in ambulance_data.values()
    current_traffic_light_order = dict(io.get_tflight_order())
    if have_ambulance:
        road_with_ambulance = get_key("HAVE AMBULANCE", ambulance_data)
        order_of_road = current_traffic_light_order[road_with_ambulance]
        await asynT.reset_ambulance_data()

        if order_of_road == "GREEN001":
            counter = 0
            suspend_counter = 0
            while True:
                suspend_counter += 1
                ambulance_have_passed = read_have_pass_flag()
                if ambulance_have_passed == "HAVE PASSED":
                    break
                if suspend_counter == 90:
                    print("Timeout error")
                    break

        elif order_of_road == "RED001":
            ambulance_counter = 0
            switch_traffic_light_two_time()
            red_transition()
            while True:
                ambulance_counter += 1
                ambulance_have_passed = read_have_pass_flag()
                if ambulance_have_passed == "HAVE PASSED":
                    switch_traffic_light_one_time()
                    break
                if ambulance_counter == 90:
                    switch_traffic_light_one_time()
                    print("Timeout error")
                    break

        elif order_of_road == "RED002":
            ambulance_counter = 0
            switch_traffic_light_one_time()
            red_transition()
            while True:
                ambulance_counter += 1
                ambulance_have_passed = read_have_pass_flag()
                if ambulance_have_passed == "HAVE PASSED":
                    switch_traffic_light_two_time()
                    break
                if ambulance_counter == 90:
                    switch_traffic_light_two_time()
                    print("Timeout error")
                    break
                else:
                    error_occured()


asyncio.run(event_loop())
