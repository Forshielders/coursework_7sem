import json

# with open('./settings/config.json') as f:
#     config = json.load(f)
    
class config_class(dict):
    __dict = {}
    
    @property
    def config(self):
        if self.__dict == {}:
            with open('./settings/config.json') as f:
                self.__dict = json.load(f)
        return self.__dict
    
    @classmethod
    def add_to_config(cls, conf:dict):
        cls.__dict.update(conf)
        
config = config_class().config

def set_config(conf: dict):
    """
    Sets the configuration by adding the provided dictionary to the config.

    Args:
        conf (dict): The dictionary containing the configuration to be added.

    Returns:
        None
    """
    config_class.add_to_config(conf)