from settings.vonfig import config
from server_side.server import server
from server_side.clasters import proxmox_claster, hadoop_claster
from server_side.vm import vm
from typing import Union
from simpy import Environment
from settings.state import state
from settings.statistic import statistic_collector
from random import randint

class common_worker:
    def __init__(self, env: Environment):
        self.time_go_for_work = config["TIME_GO_FOR_WORK"]["BASE"]
        self.time_to_work = config["TIME_TO_WORK"]["BASE"]
        self.time_to_examine = config["TIME_TO_EXAMINE"]["BASE"]
        self.can_fix = []
        self.__env = env
        self.__state = state([])
        self.statistic = statistic_collector()
        
    @property
    def state(self):
        return self.__state.state
    
    def change_state(self):
        self.__state.change_state()
        
    def fix(self, resource):
        print(f"fixing {resource.__class__.__name__} by {self.__class__.__name__}!")
        if type(resource) in self.can_fix and not resource.state_class.inner_state:
            # print("---->", resource)
            # print("---->", resource.state)
            resource.change_state()
            # print("---->", resource.state)
            print(f"timeout: {self.time_go_for_work + self.time_to_examine + self.time_to_work}")
            self.statistic.add(f"fixing_{self.__class__.__name__}", self.time_go_for_work + self.time_to_examine + self.time_to_work)
            self.statistic.add(f"count_fixing_{self.__class__.__name__}", 1)
            return self.time_go_for_work + self.time_to_examine + self.time_to_work
        else:
            print("not my job! -", self.__class__.__name__, resource.__class__.__name__, 
                  type(resource) in self.can_fix,f"in {self.can_fix}", not resource.state_class.inner_state)
            return False
            
class devops(common_worker):
    def __init__(self, env: Environment):
        super().__init__(env)
        self.time_go_for_work = config["TIME_GO_FOR_WORK"]["DEVOPS"]
        self.time_to_work = config["TIME_TO_WORK"]["DEVOPS"]
        self.time_to_examine = config["TIME_TO_EXAMINE"]["DEVOPS"]
        self.can_fix = [vm]
        
class hadoop_enj(common_worker):
    def __init__(self, env: Environment):
        super().__init__(env)
        self.time_go_for_work = config["TIME_GO_FOR_WORK"]["HADOOP_ENJ"]
        self.time_to_work = config["TIME_TO_WORK"]["HADOOP_ENJ"]
        self.time_to_examine = config["TIME_TO_EXAMINE"]["HADOOP_ENJ"]
        self.can_fix = [hadoop_claster]
        
    def fix(self, resource: vm):
        return super().fix(resource=resource.hadoop_claster)  
        
class proxmox_enj(common_worker):
    def __init__(self, env: Environment):
        super().__init__(env)
        self.time_go_for_work = config["TIME_GO_FOR_WORK"]["PROXMOX_ENJ"]
        self.time_to_work = config["TIME_TO_WORK"]["PROXMOX_ENJ"]
        self.time_to_examine = config["TIME_TO_EXAMINE"]["PROXMOX_ENJ"]
        self.can_fix = [proxmox_claster]
    
    def fix(self, resource: vm):
        return super().fix(resource.proxmox_claster)
        
class big_boy(common_worker):
    def __init__(self, env: Environment):
        super().__init__(env)
        self.time_go_for_work = config["TIME_GO_FOR_WORK"]["BIG_BOY"]
        self.time_to_work = config["TIME_TO_WORK"]["BIG_BOY"]
        self.time_to_examine = config["TIME_TO_EXAMINE"]["BIG_BOY"]
        self.can_fix = [hadoop_claster, proxmox_claster, vm]
        
class phone_support(common_worker):
    def __init__(self, env: Environment):
        super().__init__(env)
        __devopses = [devops(env) for x in range(config["WORKER_AMOUNT"]["DEVOPS"])]
        __hadoop_enjs = [hadoop_enj(env) for x in range(config["WORKER_AMOUNT"]["HADOOP_ENJ"])]
        __proxmox_enjs = [proxmox_enj(env) for x in range(config["WORKER_AMOUNT"]["PROXMOX_ENJ"])]
        __big_boys = [big_boy(env) for x in range(config["WORKER_AMOUNT"]["BIG_BOY"])]
        self.__workers = {}
        self.__workers["devops"] = __devopses
        self.__workers["hadoop_enj"] = __hadoop_enjs
        self.__workers["proxmox_enj"] = __proxmox_enjs
        self.__workers["big_boys"] = __big_boys
        self.__env = env
        
    def search_free_worker(self, worker_group: list):
        for worker in worker_group:
            if worker.state:
                return worker
        return None
        
    def deal_with_problem(self, problem):
        print("search for worker")
        for group in self.__workers:
            print("search in", group)
            # if config["RECOGNIZE_PROBLEM_CHANCE"] > randint(0, 100):
            #     if type(problem) is server:
            #         group = "big_boys"
            #     elif type(problem) is proxmox_claster:
            #         group = "proxmox_enj"
            #     elif type(problem) is hadoop_claster:
            #         group = "hadoop_enj"
            #     elif type(problem) is vm:
            #         group = "devops"
            #     else:
            #         raise Exception("unknown type of problem!")
            worker = None
            while worker is None:
                print("-->", len(self.__workers[group]), [x.state for x in self.__workers[group]])
                worker = self.search_free_worker(self.__workers[group])
                if worker:
                    break
                yield self.__env.timeout(config["TIME_TO_WAIT_FOR_WORKER"])
            print(2)
            status = worker.fix(problem)
            self.statistic.add(f"searched", 1)
                # yield self.__env.timeout(0)
            print("!", status)
            if status:
                yield self.__env.timeout(status)
                return True
            
        # raise Exception("no one can fix it!")
    
    def placeholder(self):
        yield self.__env.timeout(1)