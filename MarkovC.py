from typing import Callable, Generic, List, Dict, TypeVar
from enum import Enum
import random
import json

class MarkovCError(Exception):
    pass

class NodeIDNonexistentError(MarkovCError):
    pass

class NodeNonexistentError(MarkovCError):
    pass

class MarkovCStateType(Enum):
    Start = 0
    Node = 1
    End = 2


class MarkovC():
    def __init__(self) -> None:
        self.connections: Dict[int, List[int]] = {}
        self.node_id_lookup: Dict[str, int] = {}
        self.node_list: List[str] = []
    
    def append_node(self, node: str) -> None:
        if not node in self.node_id_lookup:
            self.node_id_lookup[node] = len(self.node_list)
            self.node_list.append(node)
    
    def get_node(self, node_id: int) -> str:
        if node_id >= len(self.node_list) or node_id < 0:
            raise NodeIDNonexistentError()
        return self.node_list[node_id]

    def get_node_id(self, node: str) -> int:
        if not node in self.node_list:
            raise NodeNonexistentError()
        return self.node_id_lookup[node]

    def add_connection(self, node_parent_id: int, node_child_id: int) -> None:
        if node_parent_id >= len(self.node_list) or node_parent_id < -1:
            raise NodeIDNonexistentError()
        if node_child_id >= len(self.node_list) or node_child_id < -1:
            raise NodeIDNonexistentError()
        if not node_parent_id in self.connections:
            self.connections[node_parent_id] = []
        self.connections[node_parent_id].append(node_child_id)
    
    def get_connections(self, node_parent_id: int) -> List[int]:
        if not node_parent_id in self.connections:
            return []
        return self.connections[node_parent_id]
    
    def dump_json(self) -> str:
        data: Dict = {
            'connections': self.connections,
            'node_list': self.node_list
        }
        return json.dumps(data, indent=2)
    
    def load_json(self, serialized_markov_c: str) -> None:
        data: Dict = json.loads(serialized_markov_c)
        self.connections.clear()
        for node_id in data['connections'].keys():
            self.connections[int(node_id)] = data['connections'][node_id]
        self.node_list = data['node_list']
        self.node_id_lookup.clear()
        for node_id in range(len(self.node_list)):
            self.node_id_lookup[self.node_list[node_id]] = node_id


class MarkovCBuilder():
    def __init__(self) -> None:
        self.markov_c: MarkovC = MarkovC()
        self.is_appending_node: bool = False
        self.last_appended_node_id: int = 0
    
    def append_node(self, node: str) -> None:
        self.markov_c.append_node(node)
        node_id: int = self.markov_c.get_node_id(node)
        if not self.is_appending_node:
            self.markov_c.add_connection(-1, node_id)
            self.is_appending_node = True
        else:
            self.markov_c.add_connection(self.last_appended_node_id, node_id)
        self.last_appended_node_id = node_id
    
    def end_append(self) -> None:
        self.is_appending_node = False
        self.markov_c.add_connection(self.last_appended_node_id, -1)
    
    def get_markov_c(self) -> MarkovC:
        return self.markov_c


class MarkovCNavigator():
    def __init__(self, markov_c: MarkovC = MarkovC()) -> None:
        self.markov_c: MarkovC = markov_c
        self.current_node_id: int = -1
        self.state_type: MarkovCStateType = MarkovCStateType.Start
    
    def set_markov_c(self, markov_c: MarkovC) -> None:
        self.markov_c = markov_c

    def travel_to_random_node(self) -> None:
        self.current_node_id = random.choice(self.get_current_node_connections())
        self.__update_state_type()
    
    def custom_travel(self, func: Callable[[List[int]], int]) -> None:
        self.current_node_id = func(self.get_current_node_connections())
        self.__update_state_type()
    
    def __update_state_type(self) -> None:
        if self.current_node_id == -1:
            self.state_type = MarkovCStateType.End
        else:
            self.state_type = MarkovCStateType.Node

    def get_current_node_connections(self) -> List[int]:
        return self.markov_c.get_connections(self.current_node_id)

    def set_current_node_id(self, node_id: int) -> None:
        self.current_node_id = node_id

    def get_current_node(self) -> str:
        return self.markov_c.get_node(self.current_node_id)

    def get_state_type(self) -> MarkovCStateType:
        return self.state_type
    
    def reset(self) -> None:
        self.current_node_id = -1
        self.state_type = MarkovCStateType.Start