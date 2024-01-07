from server_side.server import server
from server_side.vm import vm
from server_side.workers import phone_support
from settings.vonfig import config
from settings.state import state
from simpy import Environment
from datetime import datetime

class client:
    def __init__(self, env: Environment, phone_support: phone_support, server: server) -> None:
        self.__phone_support = phone_support
        self.__server = server
        self.__env = env
        self.__vms = list[vm]
        
    def __check_vms(self):
        for vm in self.__vms:
            if not vm.state:
                return False
        return True
        
    def work(self):
        if self.__check_vms():
            self.__vms.append(self.__server.create_vm(config["CLIENT_VM_CPU"], config["CLIENT_VM_DISK"]))
            self.__env.timeout(config["CLIENT_WORK_TIME"])
        else:
            start = datetime.now()
            self.__phone_support.deal_with_problem(self.__server)
            delta = datetime.now() - start
            if delta.seconds > config["CLIENT_WAIT_TIME"]:
                self.__server.delete_vm(self.__vms[0])