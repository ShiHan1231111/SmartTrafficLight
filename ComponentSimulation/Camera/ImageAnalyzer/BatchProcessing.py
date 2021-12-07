import collections
import os

from time import strftime

import cv2
import numpy as np

from ImageClass import ImageClass
from MarkoutStyle import MarkoutStyle
from Model import Model
from PathInfo import PathInfo
from SingleObjDetected import SingleObjDetected
from tracker import *


def main():
    have_gpu = False
    input_size = 256
    tracker = EuclideanDistTracker()
    path = get_path_info()
    model = instantiate_model(path, have_gpu)
    style = getStyle(model)
    print(strftime("%H:%M:%S"))

    seq = 0
    while seq < 816:
        seq = seq + 8
        img = cv2.imread(os.path.join("VideoData/FrameSet002", f"{seq+8}.jpg"))

        image_class = ImageClass(img, input_size)
        model.analyze_image(image_class)
        detected_classNames, obj_arr = postProcess(model.analysis_result, img, model, style, image_class, tracker)
        label_data_to_image(detected_classNames, image_class, style, str(seq), "FrameOutput\Output001")

    print(strftime("%H:%M:%S"))


def get_path_info():
    path = PathInfo(
        path_to_model_config="AI_Toolkit/yolov3-320.cfg",
        path_to_objs_name="AI_Toolkit/coco.names",
        path_to_wight="AI_Toolkit/yolov3-320.weights"
    )
    return path


def instantiate_model(path, have_gpu):
    model = Model(
        confidence_threshold=0.3,
        nms_threshold=0.3,
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


def postProcess(outputs, img, model, style, image_class, tracker):
    detected_classNames = []
    height, width = img.shape[:2]
    boxes = []
    classIds = []
    confidence_scores = []
    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if is_satisfied_condition(model, classId, confidence):
                # print(classId)
                w, h = int(det[2] * width), int(det[3] * height)
                x, y = int((det[0] * width) - w / 2), int((det[1] * height) - h / 2)
                boxes.append([x, y, w, h])
                classIds.append(classId)
                confidence_scores.append(float(confidence))

    # Apply Non-Max Suppression
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


def label_data_to_image(detected_classNames, image_class, style, file_name, output_dir):
    # count the frequency of detected classes
    img = image_class.image_file
    font_size = style.font_size
    font_color = style.font_color
    font_thickness = style.font_thickness
    frequency = collections.Counter(detected_classNames)
    # Draw counting texts in the frame
    cv2.putText(img, "Car:        " + str(frequency['car']), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                font_thickness)
    cv2.putText(img, "Motorbike:  " + str(frequency['motorbike']), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size,
                font_color, font_thickness)
    cv2.putText(img, "Bus:        " + str(frequency['bus']), (20, 80), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                font_thickness)
    cv2.putText(img, "Truck:      " + str(frequency['truck']), (20, 100), cv2.FONT_HERSHEY_SIMPLEX, font_size,
                font_color, font_thickness)

    cv2.imwrite(os.path.join(output_dir, f'{file_name}.jpg'), img)


def is_satisfied_condition(model, classId, confidence_score):
    condition1 = classId in model.target_class_index_arr
    condition2 = confidence_score > model.confidence_threshold
    return condition1 and condition2


main()
