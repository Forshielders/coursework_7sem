import simpy
from settings.state import state
from settings.vonfig import config
from settings.statistic import statistic_collector
from random import randint

class vm:
    def __init__(self, env: simpy.Environment, cpu, disk, proxmox_claster, hadoop_claster, server, parent_states = []):
        self.__cpu = cpu
        self.__disk = disk
        self.__env = env
        # print(cpu, "--->", parent_states)
        self.__state = state(parent_states)
        self.__proxmox_claster = proxmox_claster
        self.__hadoop_claster = hadoop_claster
        self.__server = server
        
        self.__hadoop_claster.use(disk=self.__disk)
        self.__env.process(self.try_to_break())
        self.statistic = statistic_collector()
        
    def set_number(self, number):
        self.number = number
        
    @property
    def cpu(self):
        return self.__cpu
    
    @property 
    def disk(self):
        return self.__disk
    
    @property
    def state(self):
        return self.__state.state
    
    @property
    def state_class(self):
        return self.__state
    
    @property
    def server(self):
        return self.__server
    
    @property
    def hadoop_claster(self):
        return self.__hadoop_claster
    
    @property
    def proxmox_claster(self):
        return self.__proxmox_claster
    
    def change_state(self):
        self.__state.change_state()
        if self.__state.state:
            self.__proxmox_claster.use(cpu=self.__cpu)
            self.__env.process(self.try_to_break())
        else:
            self.__proxmox_claster.free(cpu=self.__cpu)
            
    def try_to_break(self):
        while True:
            if randint(0, 100) < config["VM_BREAK_CHANCE"] and self.__state:
                self.change_state()
                # print("----> vm break")
                self.statistic.add(f"break_{self.__class__.__name__}", 1)
                return True
            else:
                yield self.__env.timeout(config["TRY_TO_BREAK_TIME"])

    def __del__(self):
        self.__hadoop_claster.free(disk=self.__disk)
        
        
class vm_deliver:
    def __init__(self, env: simpy.Environment, server):
        self.__server = server
        self.__internet_load = simpy.Container(env=env, init=config["INTERNET_CONNECTION"], capacity=config["INTERNET_CONNECTION"])
        
    @property
    def internet_load(self):
        return self.__internet_load.capacity
    
    def get_vm(self, cpu: int = 1, disk: int = 1):
        t_vm = self.__server.create_vm(cpu, disk)
        self.__internet_load.get(disk / config["INTERNET_LOAD_RATE"])
        return t_vm
    
    def return_vm(self, vm: vm):
        self.__internet_load.put(vm.disk / config["INTERNET_LOAD_RATE"])
        self.__server.delete_vm(vm)