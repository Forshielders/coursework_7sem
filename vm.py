from config import config
import simpy
from state import state
from server import server

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
        
        
class vm_delever:
    def __init__(self, env: simpy.Environment, server: server):
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