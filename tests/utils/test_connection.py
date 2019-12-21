import socket
import struct
import time

import pytest

from brain_computer_interface.utils import Connection

_PORT = 1234
_DATA = b'Hello, world!'
_CONN_DATA = struct.pack('I', 13) + _DATA


@pytest.fixture
def server():
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', _PORT))
    server.listen(1000)
    try:
        time.sleep(0.1)
        yield server
    finally:
        server.close()


def test_repr(server):
    sock = socket.socket()
    sock.connect(('127.0.0.1', _PORT))
    connection = Connection(sock)
    _, other_port = sock.getsockname()
    assert repr(connection) == f'<Connection from 127.0.0.1:{other_port} to 127.0.0.1:{_PORT}>'


def test_close(server):
    sock = socket.socket()
    sock.connect(('127.0.0.1', _PORT))
    connection = Connection(sock)
    assert not sock._closed
    connection.close()
    assert sock._closed


def test_send(server):
    sock = socket.socket()
    sock.connect(('127.0.0.1', _PORT))
    connection = Connection(sock)
    try:
        client, _ = server.accept()
        connection.send(_DATA)
    finally:
        connection.close()
    chunks = []
    while True:
        chunk = client.recv(4096)
        if not chunk:
            break
        chunks.append(chunk)
    assert b''.join(chunks) == _CONN_DATA


def test_receive(server):
    sock = socket.socket()
    sock.connect(('127.0.0.1', _PORT))
    connection = Connection(sock)
    try:
        client, _ = server.accept()
        client.sendall(_CONN_DATA)
        data = connection.receive()
        assert data == _DATA
    finally:
        connection.close()


def test_incomplete_data(server):
    sock = socket.socket()
    sock.connect(('127.0.0.1', _PORT))
    connection = Connection(sock)
    try:
        client, _ = server.accept()
        client.sendall(struct.pack('I', 2) + b'1')
        client.close()
        with pytest.raises(Exception):
            connection.receive()
    finally:
        connection.close()
