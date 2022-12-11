import json

with open('tw_hurricane_data.json', 'r') as fp:
    lines = fp.readlines()

lines = [json.loads(line) for line in lines]

new = {}
for i, line in enumerate(lines):
    new[str(i)] = line

with open('tw_hurricane_data_indexed.json', 'w') as fp:
    json.dump(new, fp)