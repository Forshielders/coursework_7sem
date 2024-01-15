from client_side.client import client
from server_side.workers import phone_support
from server_side.vm import vm_deliver
from server_side.server import server
from settings.statistic import statistic_collector
from simpy import Environment

env = Environment()
client = client(env, phone_support(env), vm_deliver(env, server(env, "server")))
env.run(until=1000)
statistic_collector.save()