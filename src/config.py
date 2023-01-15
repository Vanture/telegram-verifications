import json , os

PATH = "resources/"

CONFIG = PATH + "config.json"
MESSAGES = PATH + "messages.json"

with open(CONFIG) as f:
    config = json.load(f)

TOKEN = config["token"]

with open(MESSAGES) as f:
    messages = json.load(f)

def get_message(key: str):
    return messages[key]
