import asyncio
import os.path
import random

from datetime import datetime

from cv2 import cv2

from ComponentSimulation.Camera.CameraDevices.CapIO import *
from ComponentSimulation.Camera.CameraDevices.AsynchronousTask import AsynT
from ComponentSimulation.Camera.ImageAnalyzer.image_analyzer import analyze_image

CAM_ID = "CM001"
TLID = "TL001"
io = CapIO


async def event_loop():
    global TLID
    pathA = os.path.join(os.path.dirname(__file__), "../Configuration/SourceImage/A_LESS_CAR.png")
    # pathB = os.path.join(os.path.dirname(__file__), "../Configuration/SourceImage/A_MANY_CAR.png")
    # pathC = os.path.join(os.path.dirname(__file__), "../Configuration/SourceImage/A_NO_CAR.png")
    images_sources = [pathA]
    # img = cv2.imread(os.path.join("Aaa",str(os.path.dirname(__file__)),
    # "../Configuration/SourceImage/B_LESS_CAR.png")) img = cv2.cvtColor(img,cv2.COLOR_RGB2BGRA) cv2.imshow("yy",
    # img) cv2.waitKey()
    while True:
        try:
            print("running cam 001....")
            random_image = random.choice(images_sources)
            event, val = await asyncio.gather(AsynT.listen_capture_event(CAM_ID), AsynT.sleep(0.5))
            print(event)

            if event == "REQUEST_CAP":
                await AsynT.CAP_ACK(CAM_ID)
                print("Capturing image..........")
                img = cv2.imread(random_image)
                print("Analyzing image..........")
                frequency, total_vehicle = analyze_image(CAM_ID, img)
                order = io.get_order(TLID)
                dict_total = {"Total": total_vehicle}
                print(f"TL001 Traffic is {dict_total}")
                frequency = dict(frequency)
                complete_dict = dict_total | frequency
                print(f"Complete dict is {complete_dict}")
                print(f"TLID is {TLID}")
                complete_dict_with_timestamp = complete_dict["timestamp"] = fb.create_time_stamp()
                await asyncio.gather(
                    AsynT.update_traffic(order, total_vehicle),
                    AsynT.update_traffic_data(complete_dict_with_timestamp,TLID))
        except KeyboardInterrupt:



asyncio.run(event_loop())
