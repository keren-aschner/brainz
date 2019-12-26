import multiprocessing
import socket
import struct
import time
from datetime import datetime

import pytest
from construct import Container

from brain_computer_interface import upload_snapshot

_SERVER_ADDRESS = '127.0.0.1', 5000
_SERVER_BACKLOG = 1000

_HEADER_FORMAT = 'LL'
_HEADER_SIZE = struct.calcsize(_HEADER_FORMAT)
_FULL_CONFIG = b'\x06\x00\x00\x00\t\x00\x00\x00timestamp\x0b\x00\x00\x00translation\x08\x00\x00\x00rotation\x0b\x00' \
               + b'\x00\x00color_image\x0b\x00\x00\x00depth_image\x08\x00\x00\x00feelings'
_PARTIAL_CONFIG = b'\x05\x00\x00\x00\t\x00\x00\x00timestamp\x0b\x00\x00\x00translation\x08\x00\x00\x00rotation' \
                  + b'\x0b\x00\x00\x00color_image\x08\x00\x00\x00feelings'

_USER_1 = Container(id=1, name='Keren Solodkin', birth_date=datetime(1997, 2, 25), gender='f')
_USER_1_BIN = b'\x01\x00\x00\x00\x00\x00\x00\x00\x0e\x00\x00\x00Keren Solodkin\x80+\x123f'
_USER_2 = Container(id=2, name='Bar Aschner', birth_date=datetime(1997, 5, 22), gender='m')
_USER_2_BIN = b'\x02\x00\x00\x00\x00\x00\x00\x00\x0b\x00\x00\x00Bar Aschner\x80\x8c\x833m'
_SNAPSHOT_1 = Container(timestamp=datetime(2019, 12, 25, 12, 25), translation=Container(x=0.487, y=0.009, z=-1.13),
                        rotation=Container(x=0.789, y=-0.123, z=0.12, w=-0.827),
                        color_image=Container(height=1, width=1, image=[[149, 174, 108]]),
                        depth_image=Container(height=1, width=1, image=[1.8]),
                        feelings=Container(hunger=1, thirst=0.5, exhaustion=0.7, happiness=0.9))
_SNAPSHOT_1_BIN = b'`u\x04=o\x01\x00\x00^\xbaI\x0c\x02+\xdf?;\xdfO\x8d\x97n\x82?\x14\xaeG\xe1z\x14\xf2\xbfsh\x91\xed|' \
                  + b'?\xe9?\xb0rh\x91\xed|\xbf\xbf\xb8\x1e\x85\xebQ\xb8\xbe?\x10X9\xb4\xc8v\xea\xbf\x01\x00\x00\x00' \
                  + b'\x01\x00\x00\x00\x95\xael\x01\x00\x00\x00\x01\x00\x00\x00ff\xe6?\x00\x00\x80?\x00\x00\x00?333?f' \
                  + b'ff?'
_SNAPSHOT_1_BIN_PARTIAL = b'`u\x04=o\x01\x00\x00^\xbaI\x0c\x02+\xdf?;\xdfO\x8d\x97n\x82?\x14\xaeG\xe1z\x14\xf2\xbfsh' \
                          + b'\x91\xed|?\xe9?\xb0rh\x91\xed|\xbf\xbf\xb8\x1e\x85\xebQ\xb8\xbe?\x10X9\xb4\xc8v\xea\xbf' \
                          + b'\x01\x00\x00\x00\x01\x00\x00\x00\x95\xael\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80?' \
                          + b'\x00\x00\x00?333?fff?'
_SNAPSHOT_2 = Container(timestamp=datetime(2019, 12, 23, 10, 32), translation=Container(x=0.927, y=0.789, z=-2.46),
                        rotation=Container(x=0.167, y=-0.935, z=0.927, w=-0.25),
                        color_image=Container(height=2, width=1, image=[[27, 27, 36], [98, 163, 2]]),
                        depth_image=Container(height=2, width=2, image=[3.8, 2.1, 9.3, 4.12]),
                        feelings=Container(hunger=-1, thirst=-0.3, exhaustion=-0.5, happiness=-0.29))
_SNAPSHOT_2_BIN = b'\x00IP2o\x01\x00\x00D\x8bl\xe7\xfb\xa9\xed?sh\x91\xed|?\xe9?\xaeG\xe1z\x14\xae\x03\xc0\xc7K7\x89A' \
                  + b'`\xc5?\xecQ\xb8\x1e\x85\xeb\xed\xbfD\x8bl\xe7\xfb\xa9\xed?\x00\x00\x00\x00\x00\x00\xd0\xbf\x02' \
                  + b'\x00\x00\x00\x01\x00\x00\x00\x1b\x1b$b\xa3\x02\x02\x00\x00\x00\x02\x00\x00\x0033s@ff\x06@\xcd' \
                  + b'\xcc\x14A\n\xd7\x83@\x00\x00\x80\xbf\x9a\x99\x99\xbe\x00\x00\x00\xbf\xe1z\x94\xbe'


@pytest.fixture
def get_messages():
    parent, child = multiprocessing.Pipe()
    process = multiprocessing.Process(target=_run_server, args=(child,))
    process.start()
    parent.recv()
    try:
        def get_message():
            if not parent.poll(1):
                raise TimeoutError()
            return parent.recv()

        yield get_message
    finally:
        process.terminate()
        process.join()


@pytest.fixture
def get_messages_partial_config():
    parent, child = multiprocessing.Pipe()
    process = multiprocessing.Process(target=_run_server, args=(child, False,))
    process.start()
    parent.recv()
    try:
        def get_message():
            if not parent.poll(1):
                raise TimeoutError()
            return parent.recv()

        yield get_message
    finally:
        process.terminate()
        process.join()


def test_connection(get_messages):
    upload_snapshot(_SERVER_ADDRESS, _USER_1, _SNAPSHOT_1)
    message = get_messages()
    assert message


def test_user(get_messages):
    upload_snapshot(_SERVER_ADDRESS, _USER_1, _SNAPSHOT_1)
    hello_msg, snapshot_msg = get_messages()
    assert hello_msg == _USER_1_BIN
    upload_snapshot(_SERVER_ADDRESS, _USER_2, _SNAPSHOT_1)
    hello_msg, snapshot_msg = get_messages()
    assert hello_msg == _USER_2_BIN


def test_snapshot(get_messages):
    upload_snapshot(_SERVER_ADDRESS, _USER_1, _SNAPSHOT_1)
    hello_msg, snapshot_msg = get_messages()
    assert snapshot_msg == _SNAPSHOT_1_BIN
    upload_snapshot(_SERVER_ADDRESS, _USER_1, _SNAPSHOT_2)
    hello_msg, snapshot_msg = get_messages()
    assert snapshot_msg == _SNAPSHOT_2_BIN


def test_partial_snapshot(get_messages_partial_config):
    upload_snapshot(_SERVER_ADDRESS, _USER_1, _SNAPSHOT_1)
    hello_msg, snapshot_msg = get_messages_partial_config()
    assert snapshot_msg == _SNAPSHOT_1_BIN_PARTIAL


def _run_server(pipe, full_config=True):
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(_SERVER_ADDRESS)
    server.listen(_SERVER_BACKLOG)
    pipe.send('ready')
    with server:
        while True:
            connection, address = server.accept()
            _handle_connection(connection, pipe, full_config)


def _handle_connection(connection, pipe, full_config):
    with connection:
        length = struct.unpack('I', _receive_all(connection, 4))[0]
        hello_msg = _receive_all(connection, length)
        config = _FULL_CONFIG if full_config else _PARTIAL_CONFIG
        config_msg = struct.pack('I', len(config)) + config
        connection.send(config_msg)
        length = struct.unpack('I', _receive_all(connection, 4))[0]
        snapshot_msg = _receive_all(connection, length)
        pipe.send([hello_msg, snapshot_msg])


def _receive_all(connection, size):
    chunks = []
    while size > 0:
        chunk = connection.recv(size)
        if not chunk:
            raise RuntimeError('incomplete data')
        chunks.append(chunk)
        size -= len(chunk)
    return b''.join(chunks)


def _assert_now(timestamp):
    now = int(time.time())
    assert abs(now - timestamp) < 5
