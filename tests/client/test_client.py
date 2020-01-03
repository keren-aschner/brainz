import json
import pathlib

from brain_computer_interface import upload_sample

RESOURCES = pathlib.Path(__file__).absolute().parent.parent / 'resources' / 'client'
PROTO_SAMPLE = RESOURCES / 'sample.mind.gz'
with open(RESOURCES / 'snapshot.json', 'r') as f:
    _SNAPSHOT = json.load(f)

_USER = {'user_id': '42', 'username': 'Dan Gittik', 'birthday': 699746400, 'gender': 'MALE'}

_SERVER_ADDRESS = '127.0.0.1:5000'
_CONFIG = ['timestamp', 'pose', 'color_image', 'depth_image', 'feelings']


def test_proto_sample(requests_mock):
    requests_mock.get(f'http://{_SERVER_ADDRESS}/config', json={'config': _CONFIG})
    requests_mock.post(f'http://{_SERVER_ADDRESS}/snapshot')

    upload_sample(_SERVER_ADDRESS, PROTO_SAMPLE, True)

    data = json.loads(requests_mock.last_request.text)
    assert data['user'] == _USER
    assert data['snapshot'] == _SNAPSHOT

# TODO add test for bin protocol
