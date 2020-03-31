from typing import Tuple

from bson.json_util import dumps, loads

from .fields import SNAPSHOT, USER


def serialize(user: dict, snapshot: dict) -> bytes:
    """
    Serialize the given user and snapshot in the client-server protocol.

    :param user: The user to serialize.
    :param snapshot: The snapshot to serialize.
    :return: The serialized message.
    """
    return dumps({USER: user, SNAPSHOT: snapshot})


def deserialize(message: bytes) -> Tuple[dict, dict]:
    """
    Deserialize the given message in the client-server protocol.

    :param message: The message to deserialize.
    :return: The deserialized user and snapshot.
    """
    data = loads(message)
    return data[USER], data[SNAPSHOT]
