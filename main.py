from client_side.client import client
from server_side.workers import phone_support
from server_side.vm import vm_deliver
from server_side.server import server
from simpy import Environment

env = Environment()
client = client(env, phone_support(env), vm_deliver(env, server(env, "server")))
env.run(until=10)