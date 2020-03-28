import json
from typing import Tuple


# TODO

def serialize(user: dict, snapshot: dict) -> str:
    return json.dumps({'user': user, 'snapshot': snapshot})


def deserialize(message: str) -> Tuple[dict, dict]:
    j = json.loads(message)
    return j['user'], j['snapshot']
