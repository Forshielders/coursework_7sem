import simpy
from . import hadoop_claster, proxmox_claster, vm, config, state

class server:
    def __init__(self, env: simpy.Environment, name: str):
        self.__state = state([])
        self.__hadoop_clasters = [hadoop_claster(env, self.__state.me_and_dad()) for x in range(config["HADOOP_CLASTERS_COUNT"])]
        self.__proxmox_clasters = [proxmox_claster(env, self.__state.me_and_dad()) for x in range(config["PROXMOX_CLASTERS_COUNT"])]
        self.__env = env
        self.__vms = []
        self.name = name
    
    @property
    def state(self):
        return self.__state.state
    
    def check_proxmox_clasters(self):
        return [claster.state for claster in self.__proxmox_clasters]
    
    def check_hadoop_clasters(self):
        return [claster.state for claster in self.__hadoop_clasters]
    
    def change_state(self):
        self.__state.change_state()
        
    def create_vm(self, cpu: int, disk: int):
        # req-s to classters
        th_claster = min(self.__hadoop_clasters, key=lambda x: x.disc)
        tp_claster = min(self.__proxmox_clasters, key=lambda x: x.cpu)
        
        t_vm = vm(self.__env, cpu, disk, tp_claster, th_claster, self.__state.me_and_dad() + th_claster.state_class.me_and_dad() + tp_claster.state_class.me_and_dad())

        return t_vm
        
    def delete_vm(self, vm: vm):
        self.__vms.remove(vm)
        del vm
        
