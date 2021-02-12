import json 

class AppConfig(object):
    def __init__(self, config_json_path):
        with open(config_json_path, "r") as json_f:
            config = json.load(json_f)
            self._history_data_folder = config["history_data_folder"]
            self._app_data_folder = config["app_data_folder"]
    
    @property
    def history_data_folder(self):
        return self._history_data_folder 
    
    @property 
    def app_data_folder(self):
        return self._app_data_folder 

    
    