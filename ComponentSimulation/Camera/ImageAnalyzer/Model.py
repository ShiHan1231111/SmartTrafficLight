import null
from cv2 import cv2


class Model(object):
    def __init__(
            # parameters
            self,
            confidence_threshold,
            nms_threshold,
            path,
            class_index_arr,
            computer_have_gpu,
            input_size,
    ):
        # actions
        self.confidence_threshold = confidence_threshold
        self.nms_threshold = nms_threshold
        self.class_names_arr = get_object_name_arr(path.path_to_objs_name)
        self.target_class_index_arr = class_index_arr
        self.ai_network = cv2.dnn.readNetFromDarknet(path.path_to_model_config, path.path_to_wight)

        if computer_have_gpu:
            self.ai_network.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.ai_network.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

        self.input_size = input_size
        self.all_layers_name = self.ai_network.getLayerNames()
        self.layers_index_arr = self.ai_network.getUnconnectedOutLayers()
        self.output_name_arr = self.get_output_names_arr()
        self.analysis_result = null

    def toString(self):
        print("****************INVOKED TO STRING FOR MODEL CLASS****************")
        print(">>confidence_threshold<<")
        print(self.confidence_threshold)
        print(">>nms_threshold<<")
        print(self.nms_threshold)
        print(">>class_names_arr <<")
        print(self.class_names_arr )
        print(">>target_class_index_arr<<")
        print(self.target_class_index_arr)
        print(">>input_size<<")
        print(self.input_size)
        print(">>all_layers_name<<")
        print(self.all_layers_name)
        print(">>layers_index_arr<<")
        print(self.layers_index_arr)
        print(">>output_name_arr<<")
        print(self.output_name_arr)

    def analyze_image(self, ImageClass):
        preprocessed_img = ImageClass.preprocessed_img
        self.ai_network.setInput(preprocessed_img)
        self.analysis_result = self.ai_network.forward(self.output_name_arr)


    def get_output_names_arr(self):
        output_names = []
        for index in self.layers_index_arr:
            output_names.append(self.all_layers_name[index - 1])
        return output_names


def get_object_name_arr(path):
    classNames = open(path).read().strip().split('\n')
    return classNames


'''
Model Class
Common question:
1. What is nms_threshold?
ANS : Non-Maximal Suppression, detection probability, means => worthiness of bounding the object

2. What is setPreferableBackend()?
ANS : prioritize certain computation software like CUDA, OPENCV

3. What is setPreferableTarget()?
ANS : target device for the ai network, eg CPU GPU

4. getLayerNames(), what is it?
ANS : get all the layers name [yolo return 3 output layers]
SOURCE: https://tinyurl.com/8y3t5wbf

5. getUnconnecteddOutLayers()
ANS: Get the index of the output layers.

'''
