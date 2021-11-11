from typing import List, Dict, Union
from enum import Enum
import random

class RandomMessageMaker():
    def __init__(self) -> None:
        self.brain = {'START': [], 'TOKENS': []}

    @staticmethod
    def brain_generator(message_data: List[str]) -> Dict:
        brain: Dict = {
            'START': []
        }
        token2id: Dict = {}
        id2token: List = []

        for message in message_data:
            message_tokens: List[str] = message.split()
            past_token: str
            past_id: int
            for token_idx in range(len(message_tokens)):
                token: str = message_tokens[token_idx]
                # add token if not found
                if not token in token2id:
                    token2id[token] = len(id2token)
                    id2token.append(token)
                id: int = token2id[token]
                
                if token_idx == 0:
                    brain['START'].append(id)
                else:
                    if not past_id in brain:
                        brain[past_id] = []
                    brain[past_id].append(id)
                past_token = token
                past_id = id
            if not past_id in brain:
                brain[past_id] = []
            brain[past_id].append(-1)
        brain['TOKENS'] = id2token
        return brain

    def set_brain(self, new_brain: Dict) -> None:
        self.brain = new_brain
    
    def generate_message(self, brain: Union[Dict, None] = None) -> str:
        if brain == None:
            brain = self.brain
        message: str = ""
        id = random.choice(brain['START'])
        while (id != -1):
            message += brain['TOKENS'][id] + " "
            id = random.choice(brain[id])
        return message[:-1]