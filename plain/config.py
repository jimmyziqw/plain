import json

class Config:
    def __init__(self, config_file='..\config.json'):
        with open(config_file, 'r') as file:
            self.config = json.load(file)
            print(self.config)
            self.root_path = self.config["paths"]["image_root"]
    # def get(self, key, default=None):
    #     keys = key.split('.')
    #     value = self.config
    #     for k in keys:
    #         value = value.get(k, default)
    #         if value is default:
    #             break
    #     return value





