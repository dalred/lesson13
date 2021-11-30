import json
def read_json(name):
    with open(name, "r", encoding='utf-8') as file:
        return json.load(file)
