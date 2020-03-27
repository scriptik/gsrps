import json

def write():
    with open('config.json', 'w') as f:
        json.dump(config, f)
        f.close

def read():
    with open('config.json', 'r') as f:
        config = json.load(f)
        f.close
        return config
