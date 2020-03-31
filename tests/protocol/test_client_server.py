import pathlib

import bson

from brain_computer_interface.protocol.client_server import serialize, deserialize
from brain_computer_interface.protocol.fields import *

RESOURCES = pathlib.Path(__file__).absolute().parent.parent / 'resources' / 'protocol'

with open(RESOURCES / 'snapshot.bson', 'rb') as f:
    _SNAPSHOT = bson.loads(f.read())

_USER = {USER_ID: '42', USERNAME: 'Dan Gittik', BIRTHDAY: 699746400, GENDER: 'MALE'}


def test_serialize_deserialize():
    user, snapshot = deserialize(serialize(_USER, _SNAPSHOT))
    assert user == _USER
    assert snapshot == _SNAPSHOT
