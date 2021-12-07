class PathInfo(object):
    def __init__(
            # parameters
            self,
            path_to_model_config,
            path_to_objs_name,
            path_to_wight
    ):
        # actions
        self.path_to_model_config = path_to_model_config
        self.path_to_objs_name = path_to_objs_name
        self.path_to_wight = path_to_wight

    def toString(self):
        print("****************INVOKED TO STRING FOR PATH CLASS****************")
        print(">>path_to_model_config<<")
        print(self.path_to_model_config)
        print(">>path_to_objs_name<<")
        print(self.path_to_objs_name)
        print(">>path_to_wight<<")
        print(self.path_to_wight)
