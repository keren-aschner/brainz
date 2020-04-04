import multiprocessing
import os
import pathlib
import time
from datetime import datetime, timezone

import pytest
import requests
from bson.json_util import dumps

from brainz.protocol.fields import *
from brainz.server.server import run_server

RESOURCES = pathlib.Path(__file__).absolute().parent.parent / 'resources' / 'server'
_SERVER_HOST = '127.0.0.1'
_SERVER_PORT = 5000

_CONFIG = {TIMESTAMP, POSE}

_USER = {USER_ID: 1, USERNAME: 'Keren Solodkin', BIRTHDAY: datetime(1997, 2, 25, tzinfo=timezone.utc).timestamp(),
         GENDER: 'FEMALE'}
_TIMESTAMP = datetime(2019, 10, 25, 15, 12, 5, 228000, tzinfo=timezone.utc)
_SNAPSHOT = {TIMESTAMP: _TIMESTAMP.timestamp() * 1000, POSE: {TRANSLATION: {'x': 0.487, 'y': 0.009, 'z': -1.13},
                                                              ROTATION: {'x': 0.487, 'y': 0.009, 'z': -1.13, 'w': 2.5}}}


@pytest.fixture
def data_dir(tmp_path):
    cwd = os.getcwd()
    parent, child = multiprocessing.Pipe()
    process = multiprocessing.Process(target=_run_server, args=(child, tmp_path))
    process.start()
    parent.recv()
    try:
        yield tmp_path
    finally:
        os.chdir(cwd)
        process.terminate()
        process.join()


def test_config(data_dir):
    time.sleep(0.5)
    config = requests.get(f'http://{_SERVER_HOST}:{_SERVER_PORT}/config').json()['config']
    assert set(config) == _CONFIG


def test_snapshot(data_dir):
    time.sleep(0.5)
    response = requests.post(f'http://{_SERVER_HOST}:{_SERVER_PORT}/snapshot',
                             data=dumps({USER: _USER, 'snapshot': _SNAPSHOT}))
    assert response.status_code == 201
    f = data_dir / 'file'
    assert f.read_text() == 'publish called'


def publish(path):
    def publish_message(message):
        with open(path / 'file', 'w') as f:
            f.write('publish called')

    return publish_message


def _run_server(pipe, data_dir):
    os.chdir(RESOURCES)
    pipe.send('ready')
    run_server(_SERVER_HOST, _SERVER_PORT, publish(data_dir))


def _get_paths(data_dir, timestamp):
    directory = data_dir / f'1/{timestamp:%Y-%m-%d_%H-%M-%S-%f}'
    return directory / 'pose.json'
