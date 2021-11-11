from typing import List, Dict, Union
from enum import Enum
import random

class MarkovCStateType(Enum):
    Start = 0
    Token = 1
    End = 2

class MarkovC():
    def __init__(self) -> None:
        self.data = {-1: []}
        self.node_id_lookup: Dict = {}
        self.token_list: List = []
        self.is_appending_token: bool = False
        self.last_appended_id: int = 0
        self.node_id: int = -1
        self.state_type: MarkovCStateType = MarkovCStateType.Start
    
    def append_token(self, token: str) -> None:
        if not token in self.node_id_lookup:
            self.node_id_lookup[token] = len(token)
            self.token_list.append(token)
        id: int = self.node_id_lookup[token]
        if not self.is_appending_token:
            self.data[-1].append(id)
            self.is_appending_token = True
        else:
            self.__allocate_last_id()
            self.data[self.last_appended_id].append(id)
        self.last_appended_id = id
    
    def end_append(self) -> None:
        self.is_appending_token = False
        self.__allocate_last_id()
        self.data[self.last_appended_id].append(-1)
    
    def __allocate_last_id(self) -> None:
        if not self.last_appended_id in self.data:
            self.data[self.last_appended_id] = []
    
    def transition_random_node(self) -> None:
        self.node_id = random.choice(self.data[self.node_id])
        self.state_type = MarkovCStateType.End if self.node_id == -1 else MarkovCStateType.Start
    
    def get_node_token(self) -> str:
        return self.token_list[self.node_id]

    def get_state_type(self) -> MarkovCStateType:
        return self.state_type
    
    def reset_state(self) -> None:
        self.node_id = -1
        self.state_type = MarkovCStateType.Start


class RandomMessageMaker():
    def __init__(self) -> None:
        self.chain: MarkovC = MarkovC()

    @staticmethod
    def generate_chain(message_data: List[str]) -> Dict:
        chain: MarkovC = MarkovC()

        for message in message_data:
            message_tokens: List[str] = message.split()
            for token in message_tokens:
                chain.append_token(token)
            chain.end_append()
        return chain

    def set_chain(self, new_chain: Dict) -> None:
        self.chain = new_chain
    
    def generate_message(self, chain: Union[MarkovC, None] = None) -> str:
        if chain == None:
            chain = self.chain
        chain.reset_state()
        chain.transition_random_node()
        message: str = chain.get_node_token()
        chain.transition_random_node()
        while (chain.get_state_type() != MarkovCStateType.End):
            message += " " + chain.get_node_token()
            chain.transition_random_node()
        return message