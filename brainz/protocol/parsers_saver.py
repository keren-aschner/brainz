import json


def serialize(data: dict) -> bytes:
    """
    Serialize the data sent from the parsers to the saver.
    """
    return json.dumps(data)


def deserialize(message: bytes) -> dict:
    """
    Deserialize the data sent from the parsers to the saver.
    """
    return json.loads(message)
