import pathlib

import pytest
from bson.json_util import loads
from click.testing import CliRunner

from brainz.client import upload_sample
from brainz.client.__main__ import cli
from brainz.protocol.fields import *

RESOURCES = pathlib.Path(__file__).absolute().parent.parent / "resources" / "client"
PROTO_SAMPLE = RESOURCES / "sample.mind.gz"
BIN_SAMPLE = RESOURCES / "sample.mind"
with open(RESOURCES / "snapshot.bson", "r") as f:
    _SNAPSHOT = loads(f.read())

_USER = {USER_ID: 42, USERNAME: "Dan Gittik", BIRTHDAY: 699746400, GENDER: "MALE"}

_SERVER_HOST = "127.0.0.1"
_SERVER_PORT = 8000
_SERVER_ADDRESS = f"{_SERVER_HOST}:{_SERVER_PORT}"
_CONFIG = [TIMESTAMP, POSE, COLOR_IMAGE, DEPTH_IMAGE, FEELINGS]

SAMPLES = [
    pytest.param(PROTO_SAMPLE, True, id="protobuf"),
    pytest.param(BIN_SAMPLE, False, id="binary"),
]


@pytest.fixture()
def requests(requests_mock):
    requests_mock.get(f"http://{_SERVER_ADDRESS}/config", json={"config": _CONFIG})
    requests_mock.post(f"http://{_SERVER_ADDRESS}/snapshot")
    yield requests_mock


@pytest.mark.parametrize("sample,protobuf", SAMPLES)
def test_sample(requests, sample, protobuf):
    upload_sample(_SERVER_HOST, _SERVER_PORT, sample, protobuf)
    data = loads(requests.last_request.body)

    assert data[USER] == _USER
    assert data["snapshot"] == _SNAPSHOT


@pytest.mark.parametrize("sample,protobuf", SAMPLES)
def test_cli(requests, sample, protobuf):
    args = ["upload-sample", str(sample)]
    if not protobuf:
        args.append("--binary")

    runner = CliRunner()
    runner.invoke(cli, args)
    data = loads(requests.last_request.body)

    assert data[USER] == _USER
    assert data["snapshot"] == _SNAPSHOT


def test_exception(requests_mock):
    requests_mock.get(f"http://{_SERVER_ADDRESS}/config", json={"config": _CONFIG})
    requests_mock.post(f"http://{_SERVER_ADDRESS}/snapshot", exc=ConnectionError)

    upload_sample(_SERVER_HOST, _SERVER_PORT, PROTO_SAMPLE)
