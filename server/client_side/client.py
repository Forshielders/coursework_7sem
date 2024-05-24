from server_side.server import server
from server_side.vm import vm_deliver
from server_side.vm import vm
from server_side.workers import phone_support
from settings.vonfig import config
from settings.state import state
from settings.statistic import statistic_collector
from simpy import Environment
from random import randint

common_id = 1

class client:
    def __init__(self, env: Environment, phone_support: phone_support, deliver: vm_deliver, id: int = 1) -> None:
        self.__phone_support = phone_support
        self.__vm_deliver = deliver
        self.__env = env
        self.__vms = []
        self.process = self.__env.process(self.work())
        self.statistic = statistic_collector()
        self.statistic.add("clien_count", 1)
        self.id = id
        
    def __check_vms(self):
        for vm in self.__vms:
            if not vm.state:
                return False
        return True
    
    def __find_problem(self):
        for vm in self.__vms:
            if not vm.state:
                # # print("---->", vm.state_class.inner_state, vm.state, vm, vm.cpu, vm.state_class)
                return vm
        
    def work(self):
        while True:
            # print("->", self.__check_vms())
            self.statistic.add(f"client_vms_{self.id}", [len(self.__vms)])
            if self.__check_vms():
                self.__vms.append(self.__vm_deliver.get_vm(config["CLIENT_VM_CPU"], config["CLIENT_VM_DISK"]))
                yield self.__env.timeout(config["CLIENT_WORK_TIME"])
            else:
                start = self.__env.now
                # self.__phone_support.deal_with_problem(self.__server)
                # print("тут мы позвонили в поддержку")
                yield self.__env.process(self.__phone_support.deal_with_problem(self.__find_problem()))
                delta = self.__env.now - start
                # print(f"================> {delta} > {config["CLIENT_WAIT_TIME"]} = {delta > config["CLIENT_WAIT_TIME"]}")
                if delta > config["CLIENT_WAIT_TIME"]:
                    for vm in self.__vms:
                        self.__vm_deliver.return_vm(vm)
                    self.__vms = []
                    # break
                    
            if len(self.__vms) > config["CLIENT_EXP_COUNT"] and randint(0, 100) < config["CLIENT_EXP_CHANCE"]:
                    self.statistic.add("expanded", 1)
                    global common_id
                    common_id += 1
                    create_new_client(self.__env, self.__phone_support, self.__vm_deliver, self.id * 10 + common_id)
                        
                        
def create_new_client(env: Environment, phone_support: phone_support, deliver: vm_deliver, id: int):
    return client(env, phone_support, deliver, id)