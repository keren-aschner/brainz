import multiprocessing
import os
import pathlib
import time
from datetime import datetime, timezone

import pytest
import requests

from brain_computer_interface.server.server import run_server, Server

RESOURCES = pathlib.Path(__file__).absolute().parent.parent / 'resources' / 'server'
_SERVER_ADDRESS = '127.0.0.1', 5000

_CONFIG = {'timestamp', 'pose'}

_USER = {'user_id': '1', 'name': 'Keren Solodkin', 'birthday': datetime(1997, 2, 25, tzinfo=timezone.utc).timestamp(),
         'gender': 'FEMALE'}
_TIMESTAMP = datetime(2019, 10, 25, 15, 12, 5, 228000, tzinfo=timezone.utc)
_SNAPSHOT = {'timestamp': _TIMESTAMP.timestamp() * 1000,
             'pose': {'translation': {'x': 0.487, 'y': 0.009, 'z': -1.13}}}


@pytest.fixture
def data_dir(tmp_path):
    Server.fields = set()
    Server.processors = []
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
    host, port = _SERVER_ADDRESS
    time.sleep(1)
    config = requests.get(f'http://{host}:{port}/config').json()['config']
    assert set(config) == _CONFIG


def test_snapshot(data_dir):
    host, port = _SERVER_ADDRESS
    time.sleep(1)
    requests.post(f'http://{host}:{port}/snapshot', json={'user': _USER, 'snapshot': _SNAPSHOT})
    translation = _get_paths(data_dir, _TIMESTAMP)
    assert translation.read_text() == '{"x": 0.487, "y": 0.009, "z": -1.13}'


def _run_server(pipe, data_dir):
    os.chdir(RESOURCES)
    pipe.send('ready')
    run_server(_SERVER_ADDRESS, data_dir)


def _get_paths(data_dir, timestamp):
    directory = data_dir / f'1/{timestamp:%Y-%m-%d_%H-%M-%S-%f}'
    return directory / 'translation.json'
