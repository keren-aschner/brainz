import json
import multiprocessing
import pathlib

import pytest

from brain_computer_interface import upload_sample

RESOURCES = pathlib.Path(__file__).absolute().parent.parent / 'resources' / 'client'
PROTO_SAMPLE = RESOURCES / 'sample.mind.gz'
with open(RESOURCES / 'snapshot.json', 'r') as f:
    _SNAPSHOT = json.load(f)
_USER = {'user_id': '42', 'username': 'Dan Gittik', 'birthday': 699746400, 'gender': 'MALE'}

_SERVER_ADDRESS = '127.0.0.1', 5000
_ADDRESS = f'{_SERVER_ADDRESS[0]}:{_SERVER_ADDRESS[1]}'

_CONFIG = ['timestamp', 'pose', 'color_image', 'depth_image', 'feelings']


@pytest.fixture
def data_dir(tmp_path):
    parent, child = multiprocessing.Pipe()
    process = multiprocessing.Process(target=_run_server, args=(child, tmp_path))
    process.start()
    parent.recv()
    try:
        yield tmp_path
    finally:
        process.terminate()
        process.join()


def test_proto_sample(data_dir):
    upload_sample(_ADDRESS, PROTO_SAMPLE)
    with open(data_dir / 'user.json', 'r') as f:
        user = json.load(f)
    with open(data_dir / 'snapshot.json', 'r') as f:
        snapshot = json.load(f)

    assert user == _USER
    assert snapshot == _SNAPSHOT


# TODO add test for bin sample

def _run_server(pipe, data_dir):
    from flask import Flask, request
    from flask_restful import Resource, Api

    app = Flask(__name__)
    api = Api(app)

    class Config(Resource):
        def get(self):
            return {'config': _CONFIG}

    class Snapshot(Resource):
        def post(self):
            data = request.get_json()
            user = data['user']
            snapshot = data['snapshot']
            with open(data_dir / 'user.json', 'w+') as f:
                json.dump(user, f)
            with open(data_dir / 'snapshot.json', 'w+') as f:
                json.dump(snapshot, f)
            return {}, 201

    api.add_resource(Config, '/config')
    api.add_resource(Snapshot, '/snapshot')

    host, port = _SERVER_ADDRESS
    pipe.send('ready')
    app.run(host=host, port=port)
