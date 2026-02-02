import json

def load_feed(path):
    with open(path) as f:
        return json.load(f)

