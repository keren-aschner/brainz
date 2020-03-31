import os
from pathlib import Path

from .fields import COLOR_IMAGE, TIMESTAMP, DATA, USER_ID


def serialize_bin_data(directory: str, user: dict, snapshot: dict) -> dict:
    """
    Save the binary fields from the snapshot in a file in /opt/brain_computer_interface.

    :param directory: The directory for saving binary data.
    :param user: The user to serialize.
    :param snapshot: The snapshot to serialize.
    :return: The serialized message.
    """
    path = Path('/opt/brain_computer_interface') / directory / user[USER_ID] / str(snapshot[TIMESTAMP])
    os.makedirs(path, exist_ok=True)
    if COLOR_IMAGE in snapshot:
        path = path / f'{COLOR_IMAGE}_data.bin'
        with open(path, 'wb') as f:
            f.write(snapshot[COLOR_IMAGE][DATA])
        snapshot[COLOR_IMAGE][DATA] = str(path.absolute())
    return snapshot


def deserialize_bin_data(snapshot: dict) -> dict:
    """.
    Load the binary fields from /opt/brain_computer_interface.

    :param snapshot: The snapshot to deserialize.
    :return: The snapshot with the binary fields.
    """
    if COLOR_IMAGE in snapshot:
        with open(snapshot[COLOR_IMAGE][DATA], 'rb') as f:
            snapshot[COLOR_IMAGE][DATA] = f.read()
    return snapshot
