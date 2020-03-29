from typing import Tuple

import bson


def serialize(user: dict, snapshot: dict) -> bytes:
    """
    Serialize the given user and snapshot in the client-server protocol.

    :param user: The user to serialize.
    :param snapshot: The snapshot to serialize.
    :return: The serialized message.
    """
    return bson.dumps({'user': user, 'snapshot': snapshot})


def deserialize(message: bytes) -> Tuple[dict, dict]:
    """
    Deserialize the given message in the client-server protocol.

    :param message: The message to deserialize.
    :return: The deserialized user and snapshot.
    """
    data = bson.loads(message)
    return data['user'], data['snapshot']
