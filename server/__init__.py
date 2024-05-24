from .client_side.client import client 
from .settings.vonfig import config, set_config
from .settings.statistic import statistic_collector
from simpy import Environment
from .server_side.workers import phone_support
from .server_side.vm import vm_deliver
from .server_side.server import server
# from .

def start_simulation(clients: int, until: int = 200):
    """
    Starts the simulation of a system with the given number of clients.

    Parameters:
        clients (int): The number of clients in the system.
        until (int, optional): The time until which the simulation should run. Defaults to 200.

    Returns:
        bool: True if the simulation was successful.
    """
    
    env = Environment()
    phone_sup = phone_support(env)
    vm_deliv = vm_deliver(env, server(env, "server"))
    for i in range(clients):
        client(env, phone_sup, vm_deliv, i)
    env.run(until=until)
    statistic_collector.save()
    return True
