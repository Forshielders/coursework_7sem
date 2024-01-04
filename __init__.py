import json

with open('config.json') as f:
    config = json.load(f)
    
from clasters import *
from server import *