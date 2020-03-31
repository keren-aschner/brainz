import json
from typing import Tuple

from .common import serialize_bin_data, deserialize_bin_data
from .fields import USER, SNAPSHOT


def serialize(user: dict, snapshot: dict) -> bytes:
    """
    Serialize the given user and snapshot in the server-parsers protocol.
    Save the binary fields in a file in /opt/brain_computer_interface/server_parsers.

    :param user: The user to serialize.
    :param snapshot: The snapshot to serialize.
    :return: The serialized message.
    """
    snapshot = serialize_bin_data('server_parsers', user, snapshot)
    return json.dumps({USER: user, SNAPSHOT: snapshot})


def deserialize(message: bytes) -> Tuple[dict, dict]:
    """
    Deserialize the given message in the server-parsers protocol.
    Load the binary fields from /opt/brain_computer_interface/server_parsers.

    :param message: The message to deserialize.
    :return: The deserialized user and snapshot.
    """
    j = json.loads(message)
    snapshot = deserialize_bin_data(j[SNAPSHOT])
    return j[USER], snapshot
