from server_side.server import server
from server_side.vm import vm_deliver
from server_side.vm import vm
from server_side.workers import phone_support
from settings.vonfig import config
from settings.state import state
from settings.statistic import statistic_collector
from simpy import Environment
from datetime import datetime

class client:
    def __init__(self, env: Environment, phone_support: phone_support, deliver: vm_deliver) -> None:
        self.__phone_support = phone_support
        self.__vm_deliver = deliver
        self.__env = env
        self.__vms = []
        self.process = self.__env.process(self.work())
        self.statistic = statistic_collector()
        
    def __check_vms(self):
        for vm in self.__vms:
            if not vm.state:
                return False
        return True
    
    def __find_problem(self):
        for vm in self.__vms:
            if not vm.state:
                # print("---->", vm.state_class.inner_state, vm.state, vm, vm.cpu, vm.state_class)
                return vm
        
    def work(self):
        while True:
            print("->", self.__check_vms())
            self.statistic.add("client_vms", [len(self.__vms)])
            if self.__check_vms():
                self.__vms.append(self.__vm_deliver.get_vm(config["CLIENT_VM_CPU"], config["CLIENT_VM_DISK"]))
                yield self.__env.timeout(config["CLIENT_WORK_TIME"])
            else:
                start = self.__env.now
                # self.__phone_support.deal_with_problem(self.__server)
                print("тут мы позвонили в поддержку")
                yield self.__env.process(self.__phone_support.deal_with_problem(self.__find_problem()))
                delta = self.__env.now - start
                print(f"================> {delta} > {config["CLIENT_WAIT_TIME"]} = {delta > config["CLIENT_WAIT_TIME"]}")
                if delta > config["CLIENT_WAIT_TIME"]:
                    for vm in self.__vms:
                        self.__vm_deliver.return_vm(vm)
                    self.__vms = []
                        