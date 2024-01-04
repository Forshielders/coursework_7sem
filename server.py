import simpy
from . import hadoop_claster, proxmox_claster, vm, config

class server:
    def __init__(self, env: simpy.Environment, name: str):
        self.__state = False
        self.__hadoop_claster = hadoop_claster(env)
        self.__proxmox_claster = proxmox_claster(env)
        self.__env = env
        self.__vms = []
        self.name = name
    
    @property
    def state(self):
        return self.__state
    
    def check_clasters(self):
        if self.__hadoop_claster.check_state() and self.__proxmox_claster.check_state():
            return True
        else:
            return False
    
    def change_state(self):
        for vm in self.__vms:
            vm.state = not self.__state
        self.__state = not self.__state
        
    def create_vm(self, cpu: int, disk: int):
        # req-s to classters
        t_vm = vm(self.__env, cpu, disk)
        self.__proxmox_claster.use_resource(t_vm)
        self.__hadoop_claster.use_resource(t_vm)
        self.__vms.append(t_vm)
        return t_vm
        
        
