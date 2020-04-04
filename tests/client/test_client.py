import pathlib

from bson.json_util import loads

from brainz.client import upload_sample
from brainz.protocol.fields import *

RESOURCES = pathlib.Path(__file__).absolute().parent.parent / 'resources' / 'client'
PROTO_SAMPLE = RESOURCES / 'sample.mind.gz'
BIN_SAMPLE = RESOURCES / 'sample.mind'
with open(RESOURCES / 'snapshot.bson', 'r') as f:
    _SNAPSHOT = loads(f.read())

_USER = {USER_ID: 42, USERNAME: 'Dan Gittik', BIRTHDAY: 699746400, GENDER: 'MALE'}

_SERVER_HOST = '127.0.0.1'
_SERVER_PORT = 5000
_SERVER_ADDRESS = f'{_SERVER_HOST}:{_SERVER_PORT}'
_CONFIG = [TIMESTAMP, POSE, COLOR_IMAGE, DEPTH_IMAGE, FEELINGS]


def test_proto_sample(requests_mock):
    requests_mock.get(f'http://{_SERVER_ADDRESS}/config', json={'config': _CONFIG})
    requests_mock.post(f'http://{_SERVER_ADDRESS}/snapshot')

    upload_sample(_SERVER_HOST, _SERVER_PORT, PROTO_SAMPLE, True)

    data = loads(requests_mock.last_request.body)
    assert data[USER] == _USER
    assert data['snapshot'] == _SNAPSHOT


def test_bin_sample(requests_mock):
    requests_mock.get(f'http://{_SERVER_ADDRESS}/config', json={'config': _CONFIG})
    requests_mock.post(f'http://{_SERVER_ADDRESS}/snapshot')

    upload_sample(_SERVER_HOST, _SERVER_PORT, BIN_SAMPLE, False)
    data = loads(requests_mock.last_request.body)
    assert data[USER] == _USER
    assert data['snapshot'] == _SNAPSHOT


def test_exception(requests_mock):
    requests_mock.get(f'http://{_SERVER_ADDRESS}/config', json={'config': _CONFIG})
    requests_mock.post(f'http://{_SERVER_ADDRESS}/snapshot', exc=ConnectionError)

    upload_sample(_SERVER_HOST, _SERVER_PORT, PROTO_SAMPLE)
