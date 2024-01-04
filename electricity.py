import simpy
import random
#from server import server
from vonfig import config

class station:
    def __init__(self, env: simpy.Environment):
        self.__state = False
        self.__env = env
        self.action = env.process(self.run())

    @property
    def get_state(self):
        return self.__state

    def change_state(self):
        self.__state = not self.__state
        #server.change_state()

    def proc_break(self):
        if random.randint(0, 100) <= config["station_chance_to_break"]:
            print('break at %d' % self.__env.now)
            self.change_state()        

    def run(self):
        self.__state = True

        while True:
            if self.__state:
                print('Station start working at %d' % self.__env.now)
                yield self.__env.process(self.work(config["station_chance_to_break_time"]))
            else:
                print('Station start repairing at %d' % self.__env.now)
                yield self.__env.process(self.repair(config["station_repair_duration"]))   
            
    def work(self, duration):
        yield self.__env.timeout(duration)
        print('Proc break at %d' % self.__env.now)
        self.proc_break()

    def repair(self, duration):
        yield self.__env.timeout(duration)
        self.change_state()

class generator:
    def __init__(self, env: simpy.Environment, station1: station):
        self.__env = env
        self.action = env.process(self.run())
    
    def change_state(self):
        #server.change_state()
        pass

    def run(self):
        while True:
            if not station1.get_state:
                self.change_state()
                print("start generator work")
                yield self.__env.timeout(config["generator_work_time"])
            else:
                print("start chill generator")
                yield self.__env.process(self.chill(config["station_chance_to_break_time"]))

    def chill(self, duration):
        yield self.__env.timeout(duration)

    def chill(self, duration):
        self.change_state()
        yield self.__env.timeout(duration)

env = simpy.Environment()
station1 = station(env)
generator1 = generator(env, station1)
env.run(until=200)
