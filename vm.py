from . import config
import simpy
from state import state

class vm:
    def __init__(self, env: simpy.Environment, cpu, disk, proxmox_claster, hadoop_claster, parent_states = []):
        self.__cpu = cpu
        self.__disk = disk
        self.__env = env
        self.__state = state(parent_states)
        self.__proxmox_claster = proxmox_claster
        self.__hadoop_claster = hadoop_claster
        
        self.__hadoop_claster.use(cpu=self.__cpu)
        
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
    
    def change_state(self):
        self.__state.change_state()
        if self.__state.state:
            self.__proxmox_claster.use(cpu=self.__cpu)
        else:
            self.__proxmox_claster.free(cpu=self.__cpu)

    def __del__(self):
        self.__hadoop_claster.free(disk=self.__disk)