import null
import numpy as np

from NetworkComponent.Camera.ImageAnalyzer.ImageClass import ImageClass


class SingleObjDetected(object):

    def __init__(
            # parameters
            self,
            coordinates,
            color,
            name,
            confidence_score,
            index
    ):
        # actions
        self.coordinates = coordinates
        self.color = [int(c) for c in color]
        self.name = name
        self.confidence_score = confidence_score
        self.index = index

    def toString(self):
        print("****************INVOKED TO STRING FOR SingleObjDetected****************")
        print(">>coordinates<<")
        print(self.coordinates)
        print(">>color<<")
        print(self.color)
        print(">>name<<")
        print(self.name)


def is_satisfied_condition(model, classId, confidence_score):
    condition1 = classId in model.target_class_index_arr
    condition2 = confidence_score > model.confidence_threshold
    return condition1 and condition2


def get_obj_coordinates(det, img):
    width = ImageClass.WIDTH
    height = ImageClass.HEIGHT

    if width == null or height == null:
        ImageClass.WIDTH = (img.image_file.shape[:2])[0]
        ImageClass.HEIGHT = (img.image_file.shape[:2])[1]
        width = ImageClass.WIDTH
        height = ImageClass.HEIGHT

    w, h = int(det[2] * width), int(det[3] * height)
    x, y = int((det[0] * width) - w / 2), int((det[1] * height) - h / 2)

    return [x, y, w, h]
