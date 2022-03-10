from json import load as pyfy, dump as jsonify
from pymongo import MongoClient


def get_json(json: str) -> dict or str or list or None:
    with open("database/"+json+".json", "r") as json_read:
        return pyfy(json_read)


def set_json(json: str, content):
    with open("database/"+json+".json", "w") as json_write:
        jsonify(content, json_write)


def create_json(json: str, content: object):
    with open("database/"+json+".json", "w") as json_write:
        if content is None:
            return None
        jsonify(content, json_write)
    with open("database/"+json+".json", "r") as json_read:
        return pyfy(json_read)
