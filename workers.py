from config import config
from abc import ABC, abstractclassmethod
from server import server
from clasters import proxmox_claster, hadoop_claster
from vm import vm
from typing import Union
from simpy import Environment
from state import state
from random import randint

class common_worker(ABC):
    @abstractclassmethod
    def __init__(self, env: Environment):
        self.__time_go_for_work = config["TIME_GO_FOR_WORK"]["BASE"]
        self.__time_to_work = config["TIME_TO_WORK"]["BASE"]
        self.__time_to_examine = config["TIME_TO_EXAMINE"]["BASE"]
        self.__can_fix = []
        self.__env = env
        self.__state = state([])
        
    @property
    def state(self):
        return self.__state.state
    
    def change_state(self):
        self.__state.change_state()
        
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
    def __init__(self, env: Environment):
        __devopses = [devops(env) for x in config["WORKER_AMOUNT"]["DEVOPS"]]
        __hadoop_enjs = [hadoop_enj(env) for x in config["WORKER_AMOUNT"]["HADOOP_ENJ"]]
        __proxmox_enjs = [proxmox_enj(env) for x in config["WORKER_AMOUNT"]["PROXMOX_ENJ"]]
        __big_boys = [big_boy(env) for x in config["WORKER_AMOUNT"]["BIG_BOYS"]]
        self.__workers = {}
        self.__workers["devops"] = __devopses
        self.__workers["hadoop_enj"] = __hadoop_enjs
        self.__workers["proxmox_enj"] = __proxmox_enjs
        self.__workers["big_boys"] = __big_boys
        self.__env = env
        
    def search_free_worker(self, worker_group: list):
        for worker in worker_group:
            if not worker.state:
                return worker
        return None
        
    def deal_with_problem(self, problem: Union(server, proxmox_claster, hadoop_claster, vm)):
        for group in self.__workers:
            if config["RECOGNIZE_PROBLEM_CHANCE"] < randint(0, 100):
                if type(problem) is server:
                    group = "big_boys"
                elif type(problem) is proxmox_claster:
                    group = "proxmox_enj"
                elif type(problem) is hadoop_claster:
                    group = "hadoop_enj"
                elif type(problem) is vm:
                    group = "devops"
                else:
                    raise Exception("unknown type of problem!")
            worker = None
            while worker is None:
                worker = self.search_free_worker(self.__workers[group])
                if worker:
                    break
                self.__env.timeout(config["TIME_TO_WAIT_FOR_WORKER"])
                
            if worker.fix(problem):
                return True
            
        raise Exception("no one can fix it!")