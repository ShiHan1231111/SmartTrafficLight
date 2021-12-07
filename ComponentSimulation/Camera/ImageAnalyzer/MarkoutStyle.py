import numpy as np


class MarkoutStyle(object):
    def __init__(self,
                 font_color,
                 font_size,
                 font_thickness,
                 obj_names_arr):
        self.font_color = font_color
        self.font_size = font_size
        self.font_thickness = font_thickness
        np.random.seed(42)
        self.colors = np.random.randint(0, 255, size=(len(obj_names_arr), 3), dtype='uint8')
        
    def toString(self):
        print("****************INVOKED TO STRING FOR MARK OUT STYLE****************")
        print(">>font_color<<")
        print(self.font_color)
        print(">>font_size<<")
        print(self.font_size)
        print(">>font_thickness<<")
        print(self.font_thickness)