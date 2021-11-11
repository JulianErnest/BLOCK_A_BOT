from typing import List, Dictionary
from enum import Enum

class RandomMessageMaker():
    def __init__(self) -> None:

        pass

    """
    "START" = [],
    ... = [],
    ... = [],
    
    """

    def brain_generator(self, message_data: List[str]) -> Dictionary:
        brain: Dictionary = {
            "START": []
        }
        token2id: Dictionary = {}
        id2token: List = []

        for message in message_data:
            message_tokens: List[str] = message.split()
            past_token: str
            past_id: int
            for token_idx in range(len(message_tokens)):
                token: str = message_tokens[token_idx]
                # add token if not found
                if not token in token2id:
                    token2id[token] = token2id[len(id2token)]
                    id2token.append(token)
                id: int = token2id[token]
                
                if token_idx == 0:
                    brain["START"].append(id)
                else:
                    if not past_id in brain:
                        brain[past_id] = []
                    brain[past_id].append(id)
                past_token = token
                past_id = id
            if not past_id in brain:
                brain[past_id] = []
            brain[past_id].append(id)

        return brain