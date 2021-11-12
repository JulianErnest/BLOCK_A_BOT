import argparse
from RandomMessageMaker import RandomMessageMaker

my_parser = argparse.ArgumentParser(description='generates a markov chain profile')

my_parser.add_argument(
    'Path',
    metavar='profile',
    type=str,
    help='profile json file'
)

args = my_parser.parse_args()

input_path = args.Path

# if not os.path.isdir(input_path):
#     print('The path specified does not exist')
#     sys.exit()

profile_json: str
f = open("profiles/" + input_path, "r")
profile_json = f.read()
f.close()

RMM: RandomMessageMaker = RandomMessageMaker()
RMM.get_chain().load_json(profile_json)
print(RMM.generate_message())
