class state:
    def __init__(self, parents: list[object]):
        self.parents = list(set(parents))
        self.__state = True
        
    @property
    def state(self):
        t_state = self.__state
        for parent in self.parents:
            t_state = t_state and parent.state
        return t_state
            
    @property
    def inner_state(self):
        return self.__state
            
    def change_state(self):
        self.__state = not self.__state
        
    def me_and_dad(self):
        return state_to_list(self)
        
        
def flatten(S):
    if S == []:
        return S
    if isinstance(S[0], list):
        return flatten(S[0]) + flatten(S[1:])
    return S[:1] + flatten(S[1:])

def state_to_list(state_class: state) -> list[state]:
    # print([state_class] + state_to_list(x) for x in state_class.parents)
    return flatten([state_class] + [state_to_list(x) for x in state_class.parents])