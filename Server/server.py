from pyasn1.compat.octets import null
from AsynchronousTask import *

asynT = AsynchronousTask
STANDARD_PERIOD = 15
intelli_period = 15


async def event_loop():
    global intelli_period
    order = dict(io.get_tflight_order())
    TF_RED001, TF_RED002 = order["RED001"], order['RED002']
    while True:

        print("NEW CYCLE")
        red001_traffic, red002_traffic = "WAITING", "WAITING"

        CAM_ID1, CAM_ID2 = await asyncio.gather(
            asynT.obtain_cam_id(TF_RED001),
            asynT.obtain_cam_id(TF_RED002))

        for i in range(intelli_period):

            await asyncio.gather(asyncio.sleep(1), io.update_time(intelli_period - i))

            if i == 8:                              # data
                await asyncio.gather(
                    asynT.reset_to_wait("RED001"),
                    asynT.reset_to_wait("RED002"),
                    asynT.REQUEST_CAP(CAM_ID1),
                    asynT.REQUEST_CAP(CAM_ID2))

            if i > 8 and (red001_traffic == "WAITING" or red002_traffic == "WAITING"):
                print(red001_traffic, red002_traffic)
                red001_traffic, red002_traffic = \
                    await asyncio.gather(
                        asynT.get_traffic_amount("RED001"),
                        asynT.get_traffic_amount("RED002"))

                if red001_traffic != "WAITING" and red002_traffic != "WAITING":
                    await asyncio.gather(
                        asynT.AKC_RECEIVED_TRAFFIC_DATA("RED001"),
                        asynT.AKC_RECEIVED_TRAFFIC_DATA("RED002"))

                if red001_traffic != "WAITING":
                    await asynT.AKC_RECEIVED_TRAFFIC_DATA("RED001")

                if red002_traffic != "WAITING":
                    await asynT.AKC_RECEIVED_TRAFFIC_DATA("RED002")

        if red001_traffic == 0 and red002_traffic == 0:
            await asyncio.gather(
                asynT.async_print("Switched"),
                asynT.async_print("5sec transition....."),
                asynT.update_transition(),
                asyncio.sleep(5))

        elif red001_traffic == 0 and red002_traffic > 0:
            for i in range(2):
                _, new_order = \
                    await asyncio.gather(
                        asynT.update_tlight_to_switch_stat(),
                        asynT.switch_tlight_order())
            await asyncio.gather(
                asynT.async_print("Switched"),
                asynT.async_print("5sec transition....."),
                asynT.update_transition(),
                asyncio.sleep(5))

        elif (abs(red001_traffic - red002_traffic) <= 5) or (red002_traffic == 0 and red001_traffic != 0):
            print("pass through")
            _, new_order = \
                await asyncio.gather(
                    asynT.update_tlight_to_switch_stat(),
                    asynT.switch_tlight_order())

            order = dict(new_order)
            TF_RED001, TF_RED002 = order['RED001'], order['RED002']
            await asyncio.gather(
                asynT.async_print("Switched"),
                asynT.async_print("5sec transition....."),
                asynT.update_transition(),
                asyncio.sleep(5))

        elif red001_traffic > red002_traffic:
            percentage = red002_traffic / red001_traffic
            print(percentage)
            intelli_period = STANDARD_PERIOD * percentage


asyncio.run(event_loop())
