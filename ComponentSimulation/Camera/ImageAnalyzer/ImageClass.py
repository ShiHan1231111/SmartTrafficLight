import null as null
from cv2 import cv2


class ImageClass(object):

    HEIGHT = null
    WIDTH = null

    def __init__(
            # parameters
            self,
            image_file,
            input_size
    ):
        # actions
        self.image_file = image_file
        self.preprocessed_img = self.get_preprocess_image(input_size)

    def toString(self):
        print("****************INVOKED TO STRING FOR IMAGE CLASS****************")
        print(">>image_file<<")
        print(self.image_file)
        print(">>preprocessed_img<<")
        print(self.preprocessed_img)

    def get_preprocess_image(self,  input_size):
        blob = cv2.dnn.blobFromImage(self.image_file, 1 / 255, (input_size, input_size), [0, 0, 0], 1, crop=False)
        return blob

    def draw_obj_name_and_conf_score(self, detected_obj):
        name = detected_obj.name
        confidence_score = detected_obj.confidence_score
        color = detected_obj.color
        x = detected_obj.coordinates[0]
        y = detected_obj.coordinates[1]
        cv2.putText(self.image_file, f'{name.upper()} {int(confidence_score * 100)}%',
                    (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    def draw_bounding_box(self,detected_obj):
        x = detected_obj.coordinates[0]
        y = detected_obj.coordinates[1]
        w = detected_obj.coordinates[2]
        h = detected_obj.coordinates[3]
        color = detected_obj.color
        cv2.rectangle(self.image_file, (x, y), (x + w, y + h), color, 1)