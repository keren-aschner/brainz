import json

from typing import Tuple


# TODO

def serialize(user: dict, snapshot: dict) -> bytes:
    return json.dumps({'user': user, 'snapshot': snapshot})


def deserialize(message: bytes) -> Tuple[dict, dict]:
    j = json.loads(message)
    return j['user'], j['snapshot']
