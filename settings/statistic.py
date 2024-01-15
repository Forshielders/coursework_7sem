import json

class statistic_collector:
    statistic = {}
    name = f"stat"
    __logs = None
    @classmethod
    def add(cls, key, value):
        if key in cls.statistic:
            cls.statistic[key] += value
        else:
            cls.statistic[key] = value
            
    @classmethod
    def save(cls):
        with open(f"{cls.name}.json", 'w') as f:
            json.dump(cls.statistic, f)
            
    @classmethod
    def logs(cls):
        with open("stat.json", "r") as file:
            cls.__logs = json.load(file)      
    
    @classmethod
    @property
    def load(cls):
        if not cls.__logs:
            cls.logs()
        return cls.__logs