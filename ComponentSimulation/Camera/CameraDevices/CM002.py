import asyncio
import os.path
import random

from datetime import datetime

from cv2 import cv2

from ComponentSimulation.Camera.CameraDevices.CapIO import *
from ComponentSimulation.Camera.CameraDevices.AsynchronousTask import AsynT
from ComponentSimulation.Camera.ImageAnalyzer.image_analyzer import analyze_image

CAM_ID = "CM002"
TLID = "TL002"
io = CapIO


async def event_loop():
    pathA = os.path.join(os.path.dirname(__file__), "../Configuration/SourceImage/B_LESS_CAR.png")
    pathB =os.path.join(os.path.dirname(__file__), "../Configuration/SourceImage/B_MANY_CAR.png")
    pathC=os.path.join(os.path.dirname(__file__), "../Configuration/SourceImage/B_NO_CAR.png")
    images_sources = [pathA,pathB,pathC]
    # img = cv2.imread(os.path.join("Aaa",str(os.path.dirname(__file__)),
    # "../Configuration/SourceImage/B_LESS_CAR.png")) img = cv2.cvtColor(img,cv2.COLOR_RGB2BGRA) cv2.imshow("yy",
    # img) cv2.waitKey()
    while True:
        print("running cam 001....")
        random_image = random.choice(images_sources)
        event, val = await asyncio.gather(AsynT.listen_capture_event(CAM_ID), AsynT.sleep(0.5))
        print(event)

        if event == "REQUEST_CAP":
            await AsynT.CAP_ACK(CAM_ID)
            print("Capturing image..........")
            img = cv2.imread(random_image)
            # IMPORTANT : IF CHANGE ENVIRONMENT, HAVE TO RECONFIGURE POLYGON IN image_analyzer.py
            date_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            print("Analyzing image..........")
            frequency, total_vehicle = analyze_image(CAM_ID, img)
            order = io.get_order(TLID)
            dict_total = {"Total": total_vehicle}
            frequency = dict(frequency)
            complete_dict = dict_total | frequency
            await asyncio.gather(
                AsynT.update_traffic(order, total_vehicle),
                AsynT.update_traffic_data(TLID, date_time, complete_dict))


asyncio.run(event_loop())
