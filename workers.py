from config import config
from abc import ABC, abstractclassmethod
from server import server
from clasters import proxmox_claster, hadoop_claster
from vm import vm
from typing import Union
from simpy import Environment

class common_worker(ABC):
    @abstractclassmethod
    def __init__(self, env: Environment):
        self.__time_go_for_work = config["TIME_GO_FOR_WORK"]["BASE"]
        self.__time_to_work = config["TIME_TO_WORK"]["BASE"]
        self.__time_to_examine = config["TIME_TO_EXAMINE"]["BASE"]
        self.__can_fix = []
        self.__env = env
        
    def fix(self, resource: Union(server, proxmox_claster, hadoop_claster, vm)):
        self.__env.timeout(self.__time_go_for_work)
        self.__env.timeout(self.__time_to_examine)
        if type(resource) in self.__can_fix and not resource.state_class.inner_state:
            self.__env.timeout(self.__time_to_work)
            resource.change_state()
            return True
        else:
            print("not my job!")
            return False
            
class devops(common_worker):
    def __init__(self, env: Environment):
        super().__init__(env)
        self.__time_go_for_work = config["TIME_GO_FOR_WORK"]["DEVOPS"]
        self.__time_to_work = config["TIME_TO_WORK"]["DEVOPS"]
        self.__time_to_examine = config["TIME_TO_EXAMINE"]["DEVOPS"]
        self.__can_fix = [vm]
        
class hadoop_enj(common_worker):
    def __init__(self, env: Environment):
        super().__init__(env)
        self.__time_go_for_work = config["TIME_GO_FOR_WORK"]["HADOOP_ENJ"]
        self.__time_to_work = config["TIME_TO_WORK"]["HADOOP_ENJ"]
        self.__time_to_examine = config["TIME_TO_EXAMINE"]["HADOOP_ENJ"]
        self.__can_fix = [hadoop_claster]
        
class proxmox_enj(common_worker):
    def __init__(self, env: Environment):
        super().__init__(env)
        self.__time_go_for_work = config["TIME_GO_FOR_WORK"]["PROXMOX_ENJ"]
        self.__time_to_work = config["TIME_TO_WORK"]["PROXMOX_ENJ"]
        self.__time_to_examine = config["TIME_TO_EXAMINE"]["PROXMOX_ENJ"]
        self.__can_fix = [proxmox_claster]
        
class big_boy(common_worker):
    def __init__(self, env: Environment):
        super().__init__(env)
        self.__time_go_for_work = config["TIME_GO_FOR_WORK"]["BIG_BOY"]
        self.__time_to_work = config["TIME_TO_WORK"]["BIG_BOY"]
        self.__time_to_examine = config["TIME_TO_EXAMINE"]["BIG_BOY"]
        self.__can_fix = [hadoop_claster, proxmox_claster, vm]
        
class phone_support:
    def __init__(self):
        self.