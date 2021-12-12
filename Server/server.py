from Server.AsynchronousTask import *
from Server.ServerLogics import *

asynT = AsynchronousTask
STANDARD_PERIOD = 13
intelli_period = 13
TRANSITION_PERIOD = 3


async def event_loop():
    global intelli_period, TRANSITION_PERIOD
    TFFC_RED001 = 0
    TFFC_RED002 = 0

    while True:
        # Reinitialize value
        order = get_latest_traffic_light_order_dict()

        TFID_RED001 = order["RED001"]
        TFID_RED002 = order['RED002']

        red001_traffic = "WAITING"
        red002_traffic = "WAITING"

        is_required_compare = True
        is_required_read = True
        not_yet_capture = True

        print("NEW CYCLE")
        print(f"Intelli period is {intelli_period}")

        CAM_ID1, CAM_ID2 = await asyncio.gather(
            asynT.obtain_cam_id(TFID_RED001),
            asynT.obtain_cam_id(TFID_RED002))

        for i in range(intelli_period):
            await count_down(i)
            ambulance_data = fb.access_by_path("Server/Event/Ambulance")
            have_ambulance = 'HAVE AMBULANCE' in ambulance_data.values()

            if have_ambulance:
                await start_ambulance_cycle()

            remaining_time = intelli_period - i
            print(f"Remaining time is {remaining_time}")

            if is_time_to_capture(remaining_time, 8):

                if not_yet_capture:
                    await reset_database_and_request_cap(CAM_ID1, CAM_ID2)
                    not_yet_capture = False

                if no_data_fetched(red001_traffic, red002_traffic) and is_required_read:
                    print("LOGIC LOG : NO DATA FETCHED")
                    red001_traffic, red002_traffic = await continue_fetch_traffic_data()

                    "=================TEST========================="
                    red001_traffic = 10
                    red002_traffic = 10

                    if red001_traffic != "WAITING" and red002_traffic != "WAITING":
                        print("Assigned the flag")
                        is_required_compare = True
                        is_required_read = False

                elif all_data_fetched(red001_traffic, red002_traffic) and is_required_compare:
                    print("ALL DATA IS FETCHED")
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

        print(f"MONITOR TRAFFIC LOG: RED001 ({TFID_RED001}) traffic is {TFFC_RED001}")
        print(f"MONITOR TRAFFIC LOG: RED002 ({TFID_RED002})traffic is {TFFC_RED002}")

        TFFC_RED001, TFFC_RED002 = ensure_traffic_is_integer_data(TFFC_RED001, TFFC_RED002)

        print(f"PROGRESS LOG : BEFORE ENTER LOGIC GATE TFFC_RED001 ({TFFC_RED001}), TFFC_RED001({TFFC_RED002})")
        if both_roads_have_no_car(TFFC_RED001, TFFC_RED002):
            intelli_period = STANDARD_PERIOD
            await asynT.update_cycle_period(intelli_period)
            await proceed_without_switch(TRANSITION_PERIOD)
            print(f"PARAM CHECK LOG: TFFC_RED001 {TFFC_RED001}, TFFC_RED001 {TFFC_RED002}")
            print("LOGIC LOG : DETECTED BOTH ROAD NO CAR")

        elif road1_have_no_car_but_road2_have(TFFC_RED001, TFFC_RED002):
            intelli_period = STANDARD_PERIOD
            await asynT.update_cycle_period(intelli_period)
            await switch_road_one_times()
            await switch_road_one_times()
            await display_transition(TRANSITION_PERIOD)
            print(f"PARAM CHECK LOG: TFFC_RED001 {TFFC_RED001}, TFFC_RED001 {TFFC_RED002}")
            print("LOGIC LOG : ROAD1_HAVE_NO_CAR_BUT_ROAD2_HAVE")
            print(f"LOG OUTPUT: TRANSITION PERIOD IS {TRANSITION_PERIOD}")

        elif both_side_is_almost_equal_or_road2_no_car(TFFC_RED001, TFFC_RED002, 6):
            print("EVENT LOG: both_side_is_almost_equal_or_road2_no_car")
            print(f"PARAM CHECK LOG: TFFC_RED001 {TFFC_RED001}, TFFC_RED001 {TFFC_RED001}")
            intelli_period = STANDARD_PERIOD
            await asynT.update_cycle_period(intelli_period)
            await switch_road1_to_green()
            await display_transition(TRANSITION_PERIOD)

        elif TFFC_RED001 > TFFC_RED002:
            print("LOGIC LOG : DETECTED RED001_TRAFFIC > RED002_TRAFFIC")
            print(f"PARAM CHECK LOG: TFFC_RED001 {TFFC_RED001}, TFFC_RED002 {TFFC_RED002}")
            percentage = 1 + ((TFFC_RED001 - TFFC_RED002) / TFFC_RED001)
            print(f"OUTPUT LOG: Percentage IS {percentage}%")
            intelli_period = round(STANDARD_PERIOD * percentage)
            print(f"OUTPUT LOG: intelli_period IS {intelli_period}")
            print(f"old order is {order}")
            await asyncio.gather(asynT.update_cycle_period(intelli_period),
                                 display_transition(TRANSITION_PERIOD))
            await switch_road_one_times()
            new_order = fb.access_by_path("Server/Order")
            print("LINE EXECUTE LOG: The order is switched..... or maybe no")
            print(f"new order is {new_order}")

        elif TFFC_RED001 < TFFC_RED002:
            print(f"PARAM CHECK LOG: TFFC_RED001 {TFFC_RED001}, TFFC_RED001 {TFFC_RED001}")
            print("LOGIC LOG : DETECTED red001_traffic < red002_traffic")
            await switch_road1_to_green()
            await display_transition(TRANSITION_PERIOD)
            intelli_period = STANDARD_PERIOD
            pass

        else:
            print("ERROR OCCURRED, AI OR CAM MODULE MIGHT MALFUNCTION")
            pass

        await asynT.update_cycle_period(intelli_period)


async def reset_database_and_request_cap(CAM_ID1, CAM_ID2):
    print(f"REQUEST LOG: GOING TO REQUESTED CAM......... {CAM_ID1}")
    print(f"REQUEST LOG: GOING TO REQUESTED CAM......... {CAM_ID2}")
    await asyncio.gather(
        asynT.reset_to_wait("RED001"),
        asynT.reset_to_wait("RED002"),
        asynT.REQUEST_CAP(CAM_ID1),
        asynT.REQUEST_CAP(CAM_ID2))


async def count_down(i):
    await asyncio.gather(asyncio.sleep(1), io.update_time(intelli_period - i))


async def continue_fetch_traffic_data():
    x = asynT.get_traffic_amount("RED001")
    y = asynT.get_traffic_amount("RED002")
    return await asyncio.gather(x, y)


async def acknowledge_both_registry():
    await asyncio.gather(
        asynT.AKC_RECEIVED_TRAFFIC_DATA("RED001"),
        asynT.AKC_RECEIVED_TRAFFIC_DATA("RED002"))


async def proceed_without_switch(TRANSITION_PERIOD_ARG):
    await asyncio.gather(
        asynT.async_print("ACTION LOG: Switch without switching"),
        display_transition(TRANSITION_PERIOD_ARG))


async def display_transition(TRANSITION_PERIOD_ARG):
    taskA = asynT.async_print(f"{TRANSITION_PERIOD_ARG} sec transition.....")
    taskB = asynT.update_transition()
    taskC = asyncio.sleep(TRANSITION_PERIOD)
    await asyncio.gather(taskA, taskB, taskC)


async def skip_road1_green_turn():
    new_order = await switch_road_one_times()
    return new_order


async def switch_road_two_times():
    new_order_tf = {}
    for i in range(2):
        _, new_order_tf = \
            await asyncio.gather(
                asynT.update_tlight_to_switch_stat(),
                asynT.switch_tlight_order())
    return new_order_tf


async def switch_road_two_times_without_switch_status_updated():
    for i in range(2):
        await asyncio.gather(asynT.update_tlight_to_switch_stat())


async def switch_road_one_times():
    _, new_order = await asyncio.gather(
        asynT.update_tlight_to_switch_stat(),
        asynT.switch_tlight_order())
    return new_order


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


async def start_ambulance_cycle():
    ambulance_data = await asynT.read_ambulance_state_from_database()

    current_traffic_light_order = dict(io.get_tflight_order())
    TL_RED001 = current_traffic_light_order["RED001"]
    TL_RED002 = current_traffic_light_order["RED002"]
    TL_GREEN001 = current_traffic_light_order["GREEN001"]
    road_with_ambulance = get_key("HAVE AMBULANCE", ambulance_data)
    print(f"OUTPUT LOG: road_with_ambulance_is{road_with_ambulance}")
    order_of_road = get_key(road_with_ambulance, current_traffic_light_order)
    print(f"OUTPUT LOG:order_of_road_is {order_of_road}")
    await asynT.reset_ambulance_data()

    PROPER_AMBULANCE_ORDER = {
        "GREEN001": f"{TL_RED001}",
        "RED001": f"{TL_GREEN001}",
        "RED002": f"{TL_RED002}"
    }

    RESUME_ORDER = current_traffic_light_order

    if order_of_road == "GREEN001":
        suspend_counter = 0
        while True:
            suspend_counter += 1
            ambulance_have_passed = await asynT.check_ambulance_have_pass_flag()
            print("LOGIC LOG: Checked have passed flag for RED002")
            if ambulance_have_passed == "HAVE PASSED":
                await reset_is_pass_and_resume_prev_order(RESUME_ORDER)
                break
            if suspend_counter == 90:
                await reset_is_pass_and_resume_prev_order(RESUME_ORDER)
                print("Timeout error")
                break
            await asyncio.sleep(1)

    elif order_of_road == "RED001":
        ambulance_counter = 0
        await io.switch_to_ambulance_priority_order(PROPER_AMBULANCE_ORDER)
        await io.update_all_to_switch()
        await display_transition(TRANSITION_PERIOD)

        while True:
            ambulance_counter += 1
            ambulance_have_passed = await asynT.check_ambulance_have_pass_flag()
            print("LOGIC LOG: Checked have passed flag for RED002")
            if ambulance_have_passed == "HAVE PASSED":
                await reset_is_pass_and_resume_prev_order(RESUME_ORDER)
                break
            if ambulance_counter == 90:
                await reset_is_pass_and_resume_prev_order(RESUME_ORDER)
                print("Timeout error")
                break
            await asyncio.sleep(1)

    elif order_of_road == "RED002":
        ambulance_counter = 0
        await io.switch_to_ambulance_priority_order(PROPER_AMBULANCE_ORDER)
        await io.update_all_to_switch()
        await display_transition(TRANSITION_PERIOD)
        while True:
            ambulance_counter += 1
            ambulance_have_passed = await asynT.check_ambulance_have_pass_flag()
            print("LOGIC LOG: Checked have passed flag for RED002")
            if ambulance_have_passed == "HAVE PASSED":
                await reset_is_pass_and_resume_prev_order(RESUME_ORDER)
                break
            if ambulance_counter == 90:
                await reset_is_pass_and_resume_prev_order(RESUME_ORDER)
                print("Timeout error")
                break
            await asyncio.sleep(1)

    else:
        print("IO ERROR, THE VALUE IS NOT RECOGNIZE")


async def reset_is_pass_and_resume_prev_order(prev_order):
    await asyncio.gather(asynT.resume_the_traffic_light_to_previous_order(prev_order),
                         asynT.reset_back_is_pass_to_no_ambulance())


def get_latest_traffic_light_order_dict():
    return dict(io.get_tflight_order())


def ensure_traffic_is_integer_data(TFFC_RED001, TFFC_RED002):
    # prevent type error
    if TFFC_RED001 != "WAITING" and TFFC_RED002 == "WAITING":
        print("CAMERA FAILED TO COMPUTE ALL THE DATA, DEFAULT VALUE IS SET")
        TFFC_RED002 = TFFC_RED001

    elif TFFC_RED002 != "WAITING" and TFFC_RED001 == "WAITING":
        print("CAMERA FAILED TO COMPUTE ALL THE DATA, DEFAULT VALUE IS SET")
        TFFC_RED001 = TFFC_RED002

    elif TFFC_RED002 == "WAITING" and TFFC_RED001 == "WAITING":
        print("CAMERA FAILED TO COMPUTE ALL THE DATA, DEFAULT VALUE IS SET")
        TFFC_RED001 = 10
        TFFC_RED002 = 10
    else:
        pass
    return TFFC_RED001, TFFC_RED002


asyncio.run(event_loop())
