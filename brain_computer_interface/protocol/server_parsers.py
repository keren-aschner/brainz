import json
import os
from pathlib import Path
from typing import Tuple

from .fields import COLOR_IMAGE, TIMESTAMP, USER, SNAPSHOT, DATA


def serialize(user: dict, snapshot: dict) -> bytes:
    """
    Serialize the given user and snapshot in the server-parsers protocol.
    Save the binary fields in a file in /opt/brain_computer_interface/server_parsers.

    :param user: The user to serialize.
    :param snapshot: The snapshot to serialize.
    :return: The serialized message.
    """
    path = Path('/opt/brain_computer_interface/server_parsers') / user['user_id'] / str(snapshot[TIMESTAMP])
    os.makedirs(path, exist_ok=True)
    if COLOR_IMAGE in snapshot:
        path = path / f'{COLOR_IMAGE}_data.bin'
        with open(path, 'wb') as f:
            f.write(snapshot[COLOR_IMAGE][DATA])
        snapshot[COLOR_IMAGE][DATA] = str(path.absolute())
    return json.dumps({USER: user, SNAPSHOT: snapshot})


def deserialize(message: bytes) -> Tuple[dict, dict]:
    """
    Deserialize the given message in the server-parsers protocol.
    Load the binary fields from /opt/brain_computer_interface/server_parsers.

    :param message: The message to deserialize.
    :return: The deserialized user and snapshot.
    """
    j = json.loads(message)
    snapshot = j[SNAPSHOT]
    if COLOR_IMAGE in snapshot:
        with open(snapshot[COLOR_IMAGE][DATA], 'rb') as f:
            snapshot[COLOR_IMAGE][DATA] = f.read()
    return j[USER], snapshot
