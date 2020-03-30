import pathlib

import bson

from brain_computer_interface.protocol.server_parsers import serialize, deserialize

RESOURCES = pathlib.Path(__file__).absolute().parent.parent / 'resources' / 'protocol'

_USER = {'user_id': '42', 'username': 'Dan Gittik', 'birthday': 699746400, 'gender': 'MALE'}


def test_serialize_deserialize():
    with open(RESOURCES / 'snapshot.bson', 'rb') as f:
        _SNAPSHOT = bson.loads(f.read())
    user, snapshot = deserialize(serialize(_USER, _SNAPSHOT))
    assert user == _USER
    with open(RESOURCES / 'snapshot.bson', 'rb') as f:
        _SNAPSHOT = bson.loads(f.read())
    assert snapshot == _SNAPSHOT
