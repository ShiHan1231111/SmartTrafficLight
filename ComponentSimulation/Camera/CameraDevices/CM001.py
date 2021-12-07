import asyncio

from datetime import date, datetime
from NetworkComponent.Camera.CameraDevices.CapIO import *
from NetworkComponent.Camera.CameraDevices.AsynchronousTask import AsynT
from NetworkComponent.Camera.ImageAnalyzer.image_analyzer import analyze_image

CAM_ID = "CM001"
TLID = "TL001"
io = CapIO


async def event_loop():
    while True:
        event, val = await asyncio.gather(AsynT.listen_capture_event(CAM_ID), AsynT.sleep(0.5))
        ack, img = await asyncio.gather(AsynT.CAP_ACK(CAM_ID),
                                        AsynT.capture_img("..\\ImageAnalyzer", "traffic.jpg"))
        # IMPORTANT : IF CHANGE ENVIRONMENT, HAVE TO RECONFIGURE POLYGON IN image_analyzer.py
        date_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        frequency, total_vehicle = analyze_image(CAM_ID, img)
        order = io.get_order(TLID)
        key = TLID + " "+ date_time
        print(key)
        dict_total = {"Total": total_vehicle}
        frequency = dict(frequency)
        complete_dict = dict_total | frequency
        await asyncio.gather(AsynT.update_traffic(order, total_vehicle), AsynT.update_traffic_data(key,complete_dict))


asyncio.run(event_loop())
