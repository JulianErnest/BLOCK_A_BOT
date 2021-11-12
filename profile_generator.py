import argparse
import io
import json
from typing import List
from MarkovC import MarkovC
from RandomMessageMaker import RandomMessageMaker

my_parser = argparse.ArgumentParser(
    description='generates a markov chain profile'
)

my_parser.add_argument(
    'Path',
    metavar='data',
    type=str,
    help='message data json file'
)

args = my_parser.parse_args()

input_path = args.Path

# if not os.path.isdir(input_path):
#     print('The path specified does not exist')
#     sys.exit()

messages: List[str]
f = open("data/" + input_path, "r")
messages = json.loads(f.read())['messages']
f.close()

RMM: RandomMessageMaker = RandomMessageMaker()
RMM.generate_chain(messages)
chain: MarkovC = RMM.get_chain()

with io.open("profiles/" + input_path, 'w') as f:
    f.write(chain.dump_json())
