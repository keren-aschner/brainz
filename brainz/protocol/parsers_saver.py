import json


def serialize(data: dict) -> str:
    """
    Serialize the data sent from the parsers to the saver.
    """
    return json.dumps(data)


def deserialize(message: str) -> dict:
    """
    Deserialize the data sent from the parsers to the saver.
    """
    return json.loads(message)
