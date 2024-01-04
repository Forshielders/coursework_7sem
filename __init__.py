import json

with open('config.json') as f:
    config = json.load(f)
    
from clasters import *
from state import state, state_to_list
from server import *
from vm import *