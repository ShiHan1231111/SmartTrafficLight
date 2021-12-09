import collections
import os
import numpy as np
import matplotlib.pyplot as plt

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from datetime import datetime
from cv2 import cv2
from ComponentSimulation.Camera.ImageAnalyzer.ImageClass import ImageClass
from ComponentSimulation.Camera.ImageAnalyzer.MarkoutStyle import MarkoutStyle
from ComponentSimulation.Camera.ImageAnalyzer.Model import Model
from ComponentSimulation.Camera.ImageAnalyzer.PathInfo import PathInfo
from ComponentSimulation.Camera.ImageAnalyzer.SingleObjDetected import SingleObjDetected


def analyze_image(CAM_ID, img):
    have_gpu = False
    input_size = 320
    path = get_path_info()
    model = instantiate_model(path, have_gpu)
    style = getStyle(model)
    # IMPORTANT : IF IMPLEMENT NEW ENVIRONMENT, PLS RECONFIGURE THE POLYGON
    # plt.imshow(img)
    # plt.show()
    image_class = ImageClass(img, input_size)
    model.analyze_image(image_class)
    if CAM_ID == "CM001":
        polygon_of_road = np.array([[0,535],[637,134],[673,144],[701,200],[745,373],[623,719],[1,719]], np.int32)
    else:
        polygon_of_road = np.array([[1275, 719], [616, 719],[524, 376],[588, 163],[647, 148]],
                                   np.int32)
    detected_classNames, obj_arr = postProcess(model.analysis_result, img, model, style, image_class, polygon_of_road)
    frequency, total_vehicle = label_data_to_image(detected_classNames, image_class, style, polygon_of_road, CAM_ID)
    return frequency, total_vehicle


def get_path_info():
    path = PathInfo(
        path_to_model_config="../ImageAnalyzer/AI_Toolkit/yolov3-320.cfg",
        path_to_objs_name="../ImageAnalyzer/AI_Toolkit/coco.names",
        path_to_wight="../ImageAnalyzer/AI_Toolkit/yolov3-320.weights"
    )
    return path


def instantiate_model(path, have_gpu):
    model = Model(
        confidence_threshold=0.2,
        nms_threshold=0.2,
        path=path,
        class_index_arr=[2, 3, 5, 7],
        computer_have_gpu=have_gpu,
        input_size=320,
    )
    return model


def getStyle(model):
    style = MarkoutStyle(
        font_color=(0, 0, 255),
        font_size=0.5,
        font_thickness=2,
        obj_names_arr=model.class_names_arr
    )
    return style


def postProcess(outputs, img, model, style, image_class, polygon_of_road):
    detected_classNames = []
    height, width = img.shape[:2]
    boxes = []
    classIds = []
    confidence_scores = []
    polygon = Polygon(polygon_of_road)
    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if is_satisfied_condition(model, classId, confidence):
                w, h = int(det[2] * width), int(det[3] * height)
                x, y = int((det[0] * width) - w / 2), int((det[1] * height) - h / 2)
                in_shape = [polygon.contains(Point(x, y)),
                            polygon.contains(Point(x + w, y)),
                            polygon.contains(Point(x, y + h)),
                            polygon.contains(Point(x + w, y + h))]
                if in_shape.count(True) >= 3:
                    boxes.append([x, y, w, h])
                    classIds.append(classId)
                    confidence_scores.append(float(confidence))
    indices = cv2.dnn.NMSBoxes(boxes, confidence_scores, model.confidence_threshold, model.nms_threshold)
    obj_arr = []
    if len(indices) > 0:
        for i in indices.flatten():
            coordinate = [boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3]]
            color = [int(c) for c in style.colors[classIds[i]]]
            name = model.class_names_arr[classIds[i]]
            detected_classNames.append(name)
            index = model.target_class_index_arr.index(classIds[i])
            tempObj = SingleObjDetected(coordinate, color, name, confidence_scores[i], index)
            image_class.draw_obj_name_and_conf_score(tempObj)
            image_class.draw_bounding_box(tempObj)
            obj_arr.append(tempObj)
        return detected_classNames, obj_arr


def label_data_to_image(detected_classNames, image_class, style, polygon_of_road, CAM_ID):
    # count the frequency of detected classes
    img = image_class.image_file
    font_size = style.font_size
    font_color = style.font_color
    font_thickness = style.font_thickness
    frequency = collections.Counter(detected_classNames)
    total_vehicle = sum(frequency.values())
    cv2.putText(img, "Car:        " + str(frequency['car']), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                font_thickness)
    cv2.putText(img, "Motorbike:  " + str(frequency['motorbike']), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size,
                font_color, font_thickness)
    cv2.putText(img, "Bus:        " + str(frequency['bus']), (20, 80), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                font_thickness)
    cv2.putText(img, "Truck:      " + str(frequency['truck']), (20, 100), cv2.FONT_HERSHEY_SIMPLEX, font_size,
                font_color, font_thickness)
    img = cv2.polylines(img, [polygon_of_road.reshape((-1, 1, 2))], isClosed=True, color=(255, 0, 0), thickness=2)
    output_dir = f"../Gallery/{CAM_ID}/{datetime.today().strftime('%Y-%m-%d')}"
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    cv2.imwrite(os.path.join(output_dir, f'{datetime.now().strftime("H%H_M%M_S%S")}.png'), img)
    return frequency, total_vehicle


def is_satisfied_condition(model, classId, confidence_score):
    condition1 = classId in model.target_class_index_arr
    condition2 = confidence_score > model.confidence_threshold
    return condition1 and condition2
