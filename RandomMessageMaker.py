from typing import List, Dict, Union
from MarkovC import MarkovC, MarkovCStateType, MarkovCNavigator, MarkovCBuilder

class RandomMessageMaker():
    def __init__(self) -> None:
        self.chain: MarkovC = MarkovC()

    def generate_chain(self, message_data: List[str]):
        builder: MarkovCBuilder = MarkovCBuilder()

        for message in message_data:
            message_tokens: List[str] = message.split()
            for token in message_tokens:
                builder.append_node(token)
            builder.end_append()
        self.chain = builder.get_markov_c()

    def set_chain(self, new_chain: Dict) -> None:
        self.chain = new_chain
    
    def get_chain(self) -> MarkovC:
        return self.chain
    
    def generate_message(self, markov_c: Union[MarkovC, None] = None) -> str:
        if markov_c == None:
            markov_c = self.chain
        
        navigator: MarkovCNavigator = MarkovCNavigator(markov_c)
        navigator.travel_to_random_node()
        message: str = navigator.get_current_node()
        navigator.travel_to_random_node()
        while (navigator.get_state_type() != MarkovCStateType.End):
            message += " " + navigator.get_current_node()
            navigator.travel_to_random_node()
        return message