import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config(object):
    def __init__(self):
        self.CONFIG_FOLDER_PATH = os.path.join(BASE_DIR, "config")
        self.CONFIG_FILES_NAME = self.list_config_files()
        self.CONFIG_JSON = {}
        self.read_config()

    def get_value(self, key):
        if key in self.CONFIG_JSON:
            if "path" in key:
                return os.path.expanduser(self.CONFIG_JSON[key])
            return self.CONFIG_JSON[key]
        else:
            raise KeyError("{} is not in Config.".format(key))

    def read_config(self):
        for config_file_name in self.CONFIG_FILES_NAME:
            file_path = self.get_config_file_path(config_file_name)
            if 'template' in file_path:
                print(file_path)
                continue
            if os.path.isfile(file_path):
                with open(file_path, "r") as json_file:
                    self.CONFIG_JSON = {**self.CONFIG_JSON, **json.loads(json_file.read())}
            else:
                raise FileNotFoundError("{} not exist.".format(file_path))

    def get_config_file_path(self, config_file_name):
        return os.path.join(self.CONFIG_FOLDER_PATH, config_file_name)

    def list_config_files(self):
        return os.listdir(self.CONFIG_FOLDER_PATH)
