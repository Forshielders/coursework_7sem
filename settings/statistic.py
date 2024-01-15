import json

class statistic_collector:
    statistic = {}
    name = f"stat"
    @classmethod
    def add(cls, key, value):
        if key in cls.statistic:
            cls.statistic[key] += value
        else:
            cls.statistic[key] = value
            
    @classmethod
    def save(self):
        with open(f"{self.name}.json", 'w') as f:
            json.dump(self.statistic, f)