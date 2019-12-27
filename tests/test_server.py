import json
import multiprocessing
import pathlib
import socket
import struct
import time
from datetime import datetime

import pytest

from brain_computer_interface.processors.processor import Processor
from brain_computer_interface.server import run_server, Server

_SERVER_ADDRESS = '127.0.0.1', 5000

_TIMESTAMP = datetime(2019, 10, 25, 15, 12, 5, 228000)
_USER_BIN = b'\x01\x00\x00\x00\x00\x00\x00\x00\x0e\x00\x00\x00Keren Solodkin\x80+\x123f'
_CONFIG = [b'\x02\x00\x00\x00\t\x00\x00\x00timestamp\x0b\x00\x00\x00translation',
           b'\x02\x00\x00\x00\x0b\x00\x00\x00translation\t\x00\x00\x00timestamp']

with open(pathlib.Path(__file__).absolute().parent / 'resources' / 'snapshot.bin', 'rb') as f:
    _SNAPSHOT_BIN = f.read()


@pytest.fixture
def data_dir(tmp_path):
    Server.processors = []
    Server.fields = set()

    @Server.processor('timestamp', 'translation')
    class TranslationProcessor(Processor):
        def process(self, snapshot):
            translation = dict(snapshot.translation)
            translation.pop('_io', None)
            with open(self.get_dir(snapshot.timestamp) / 'translation.json', 'w+') as f:
                json.dump(translation, f)

    parent, child = multiprocessing.Pipe()
    process = multiprocessing.Process(target=_run_server, args=(child, tmp_path))
    process.start()
    parent.recv()
    try:
        yield tmp_path
    finally:
        process.terminate()
        process.join()


def test_server(data_dir):
    config = _handle_connection(_USER_BIN, _SNAPSHOT_BIN)
    assert config in _CONFIG
    translation = _get_paths(data_dir, _TIMESTAMP)

    assert translation.read_text() == '{"x": 0.487, "y": 0.009, "z": -1.13}'


def _run_server(pipe, data_dir):
    pipe.send('read')
    run_server(_SERVER_ADDRESS, data_dir)


def _handle_connection(user_bin, snapshot_bin):
    with socket.socket() as connection:
        time.sleep(0.1)  # Wait for server to start listening.
        connection.settimeout(2)
        connection.connect(_SERVER_ADDRESS)

        hello = struct.pack('I', len(user_bin)) + user_bin
        connection.sendall(hello)
        length = struct.unpack('I', _receive_all(connection, 4))[0]
        config = _receive_all(connection, length)
        snapshot = struct.pack('I', len(snapshot_bin)) + snapshot_bin
        connection.sendall(snapshot)

    time.sleep(0.1)  # Wait for server to process
    return config


def _receive_all(connection, size):
    chunks = []
    while size > 0:
        chunk = connection.recv(size)
        if not chunk:
            raise RuntimeError('incomplete data')
        chunks.append(chunk)
        size -= len(chunk)
    return b''.join(chunks)


def _get_paths(data_dir, timestamp):
    directory = data_dir / f'1/{timestamp:%Y-%m-%d_%H-%M-%S-%f}'
    return directory / 'translation.json'
