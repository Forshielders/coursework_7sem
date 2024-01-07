class state:
    def __init__(self, parents: list[object]):
        self.parents = list(set(parents))
        self.__state = True
        
    @property
    def state(self):
        t_state = self.__state
        for parent in state_to_list(self):
            t_state = t_state and parent.state
            
    @property
    def inner_state(self):
        return self.__state
            
    def change_state(self):
        self.__state = not self.__state
        
    def me_and_dad(self):
        return state_to_list(self)
        
def state_to_list(state_class: state) -> list[state]:
    return [state_to_list(x) for x in state_class.parents]