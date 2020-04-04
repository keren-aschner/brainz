import pathlib

from bson.json_util import loads

from brainz.protocol.fields import *
from brainz.protocol.server_parsers import serialize, deserialize

RESOURCES = pathlib.Path(__file__).absolute().parent.parent / 'resources' / 'protocol'

_USER = {USER_ID: 42, USERNAME: 'Dan Gittik', BIRTHDAY: 699746400, GENDER: 'MALE'}


def test_serialize_deserialize():
    with open(RESOURCES / 'snapshot.bson', 'rb') as f:
        _SNAPSHOT = loads(f.read())
    user, snapshot = deserialize(serialize(_USER, _SNAPSHOT))
    assert user == _USER
    with open(RESOURCES / 'snapshot.bson', 'rb') as f:
        _SNAPSHOT = loads(f.read())
    assert snapshot == _SNAPSHOT
