import json


# TODO

def serialize(data: dict) -> bytes:
    return json.dumps(data)


def deserialize(message: bytes) -> dict:
    return json.loads(message)
