import simpy
from settings.vonfig import config
from server_side.vm import vm  
from settings.state import state
from random import randint

class claster:
    def __init__(self, env: simpy.Environment, parent_states = []):
        self.__state = state(parent_states)
        self.__env = env
        self.__vms = list[vm]
        # self.action = self.__env.process(self.try_to_break())
        
    @property
    def state(self):
        return self.__state.state
    
    @property
    def state_class(self):
        return self.__state
    
    def change_state(self):
        self.__state.change_state()
    
    def try_to_break(self):
        if randint(0, 100) < config["CLASTER_BREAK_CHANCE"] and not self.__state:
            self.change_state()
            return True
        else:
            self.__env.timeout(config["TRY_TO_BREAK_TIME"])
            
    def add_vm(self, vm: vm):
        self.__vms.append(vm)

class hadoop_claster(claster):
    def __init__(self, env: simpy.Environment, parent_states = []):
        super().__init__(env=env, parent_states=parent_states)
        self.__disk = simpy.Container(env=env, init=config["HADOOP_CLASTER_DISK"], capacity=config["HADOOP_CLASTER_DISK"])
        
    @property
    def disc(self):
        return self.__disk.level
    
    def use(self, vm: vm = None, disk: int = None):
        if vm: 
            self.__disk.get(vm.disk)
        else:
            self.__disk.get(disk)
        
    def free(self, vm: vm = None, disk: int = None):
        if vm:
            self.__disk.put(vm.disk)
        else:
            self.__disk.put(disk)

class proxmox_claster(claster):
    def __init__(self, env, parent_states = []):
        super().__init__(env=env, parent_states=parent_states)
        self.__cpu = simpy.Container(env=env, init=config["PROXMPX_CLASTER_CPU"], capacity=config["PROXMPX_CLASTER_CPU"])
        
    @property
    def cpu(self):
        return self.__cpu.level
    
    def use(self, vm: vm = None, cpu: int = None):
        if vm:
            self.__cpu.get(vm.cpu)
        else:
            self.__cpu.get(cpu)
        
    def free(self, vm: vm = None, cpu: int = None):
        if vm:
            self.__cpu.put(vm.cpu)
        else:
            self.__cpu.put(cpu)